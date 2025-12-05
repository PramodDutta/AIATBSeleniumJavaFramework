package com.automation.base;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.testng.ITestResult;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Parameters;

import java.time.Duration;

public class BaseTest {

    protected WebDriver driver;
    protected static final Logger logger = LogManager.getLogger(BaseTest.class);

    // Default test URL - can be overridden via config
    protected static final String BASE_URL = "https://practicetestautomation.com/practice-test-login/";

    @BeforeMethod
    @Parameters({ "browser" })
    public void setUp(String browser) {
        logger.info("Setting up WebDriver for browser: " + browser);
        initializeDriver(browser);
        driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        driver.get(BASE_URL);
        logger.info("Navigated to: " + BASE_URL);
    }

    private void initializeDriver(String browser) {
        if (browser == null || browser.isEmpty()) {
            browser = "chrome";
        }

        // Selenium 4.6+ has built-in Selenium Manager - no need for WebDriverManager
        switch (browser.toLowerCase()) {
            case "chrome":
                ChromeOptions options = new ChromeOptions();
                options.addArguments("--remote-allow-origins=*");
                driver = new ChromeDriver(options);
                break;
            case "firefox":
                driver = new FirefoxDriver();
                break;
            default:
                logger.warn("Browser not supported, defaulting to Chrome");
                driver = new ChromeDriver();
        }
        logger.info("WebDriver initialized successfully");
    }

    @AfterMethod
    public void tearDown(ITestResult result) {
        // Screenshot capture is handled by AllureScreenshotListener
        if (result.getStatus() == ITestResult.FAILURE) {
            logger.error("Test failed: " + result.getName());
        }
        if (driver != null) {
            logger.info("Closing browser");
            driver.quit();
        }
    }
}
