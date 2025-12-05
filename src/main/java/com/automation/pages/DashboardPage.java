package com.automation.pages;

import com.automation.base.BasePage;
import io.qameta.allure.Step;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

public class DashboardPage extends BasePage {

    // Page Elements
    @FindBy(css = ".post-title")
    private WebElement successMessage;

    @FindBy(linkText = "Log out")
    private WebElement logoutButton;

    @FindBy(css = ".has-text-align-center strong")
    private WebElement welcomeMessage;

    public DashboardPage(WebDriver driver) {
        super(driver);
        logger.info("DashboardPage initialized");
    }

    @Step("Check if success message is displayed")
    public boolean isSuccessMessageDisplayed() {
        logger.info("Checking if success message is displayed");
        return isElementDisplayed(successMessage);
    }

    @Step("Get success message text")
    public String getSuccessMessageText() {
        logger.info("Getting success message text");
        return getText(successMessage);
    }

    @Step("Check if logout button is displayed")
    public boolean isLogoutButtonDisplayed() {
        logger.info("Checking if logout button is displayed");
        return isElementDisplayed(logoutButton);
    }

    @Step("Click logout button")
    public LoginPage clickLogout() {
        logger.info("Clicking logout button");
        click(logoutButton);
        return new LoginPage(driver);
    }

    @Step("Verify user is on dashboard page")
    public boolean isOnDashboardPage() {
        logger.info("Verifying user is on dashboard page");
        return getCurrentUrl().contains("logged-in-successfully") || 
               getCurrentUrl().contains("practicetestautomation.com/logged-in-successfully");
    }

    @Step("Get welcome message")
    public String getWelcomeMessage() {
        logger.info("Getting welcome message");
        return getText(welcomeMessage);
    }
}

