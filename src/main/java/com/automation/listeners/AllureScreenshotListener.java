package com.automation.listeners;

import io.qameta.allure.Allure;
import io.qameta.allure.Attachment;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.testng.ITestListener;
import org.testng.ITestResult;

import java.io.ByteArrayInputStream;
import java.lang.reflect.Field;

/**
 * TestNG Listener for Allure screenshot capture on test failures.
 * Automatically captures screenshot and page source when a test fails.
 */
public class AllureScreenshotListener implements ITestListener {

    private static final Logger logger = LogManager.getLogger(AllureScreenshotListener.class);

    @Override
    public void onTestFailure(ITestResult result) {
        logger.info("Test failed: " + result.getName() + " - Capturing screenshot for Allure");
        
        WebDriver driver = getDriverFromTestClass(result);
        if (driver != null) {
            captureScreenshot(driver, result.getName());
            capturePageSource(driver, result.getName());
            captureCurrentUrl(driver);
        } else {
            logger.warn("Could not get WebDriver instance for screenshot capture");
        }
    }

    @Override
    public void onTestSkipped(ITestResult result) {
        logger.info("Test skipped: " + result.getName());
    }

    /**
     * Capture screenshot and attach to Allure report.
     */
    private void captureScreenshot(WebDriver driver, String testName) {
        try {
            byte[] screenshot = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
            Allure.addAttachment(
                    testName + "_failure_screenshot",
                    "image/png",
                    new ByteArrayInputStream(screenshot),
                    ".png"
            );
            logger.info("Screenshot captured and attached to Allure report");
        } catch (Exception e) {
            logger.error("Failed to capture screenshot: " + e.getMessage());
        }
    }

    /**
     * Capture page source and attach to Allure report.
     */
    private void capturePageSource(WebDriver driver, String testName) {
        try {
            String pageSource = driver.getPageSource();
            Allure.addAttachment(
                    testName + "_page_source",
                    "text/html",
                    pageSource
            );
            logger.info("Page source captured and attached to Allure report");
        } catch (Exception e) {
            logger.error("Failed to capture page source: " + e.getMessage());
        }
    }

    /**
     * Capture current URL and attach to Allure report.
     */
    private void captureCurrentUrl(WebDriver driver) {
        try {
            String currentUrl = driver.getCurrentUrl();
            Allure.addAttachment("Current URL", "text/plain", currentUrl);
            logger.info("Current URL captured: " + currentUrl);
        } catch (Exception e) {
            logger.error("Failed to capture current URL: " + e.getMessage());
        }
    }

    /**
     * Get WebDriver instance from the test class using reflection.
     */
    private WebDriver getDriverFromTestClass(ITestResult result) {
        Object testInstance = result.getInstance();
        Class<?> clazz = testInstance.getClass();

        // Search through class hierarchy for 'driver' field
        while (clazz != null) {
            try {
                Field driverField = clazz.getDeclaredField("driver");
                driverField.setAccessible(true);
                Object driverObj = driverField.get(testInstance);
                if (driverObj instanceof WebDriver) {
                    return (WebDriver) driverObj;
                }
            } catch (NoSuchFieldException e) {
                // Field not in this class, try superclass
                clazz = clazz.getSuperclass();
            } catch (IllegalAccessException e) {
                logger.error("Cannot access driver field: " + e.getMessage());
                return null;
            }
        }
        return null;
    }

    /**
     * Attachment method for screenshot - alternative approach using @Attachment annotation.
     */
    @Attachment(value = "Screenshot on Failure", type = "image/png")
    public byte[] saveScreenshot(WebDriver driver) {
        return ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
    }

    /**
     * Attachment method for page source - alternative approach using @Attachment annotation.
     */
    @Attachment(value = "Page Source on Failure", type = "text/html")
    public String savePageSource(WebDriver driver) {
        return driver.getPageSource();
    }
}

