package com.automation.pages;

import com.automation.base.BasePage;
import io.qameta.allure.Step;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

public class LoginPage extends BasePage {

    // Page Elements
    @FindBy(id = "username")
    private WebElement usernameField;

    @FindBy(id = "password")
    private WebElement passwordField;

    @FindBy(id = "submit")
    private WebElement submitButton;

    @FindBy(id = "error")
    private WebElement errorMessage;

    public LoginPage(WebDriver driver) {
        super(driver);
        logger.info("LoginPage initialized");
    }

    @Step("Enter username: {username}")
    public LoginPage enterUsername(String username) {
        logger.info("Entering username: " + username);
        sendKeys(usernameField, username);
        return this;
    }

    @Step("Enter password")
    public LoginPage enterPassword(String password) {
        logger.info("Entering password");
        sendKeys(passwordField, password);
        return this;
    }

    @Step("Click submit button")
    public void clickSubmit() {
        logger.info("Clicking submit button");
        click(submitButton);
    }

    @Step("Login with username: {username} and password")
    public DashboardPage loginAs(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        clickSubmit();
        logger.info("Login attempted with username: " + username);
        return new DashboardPage(driver);
    }

    @Step("Login with invalid credentials: {username}")
    public LoginPage loginWithInvalidCredentials(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        clickSubmit();
        logger.info("Login attempted with invalid credentials");
        return this;
    }

    @Step("Get error message")
    public String getErrorMessage() {
        logger.info("Getting error message");
        return getText(errorMessage);
    }

    @Step("Check if error message is displayed")
    public boolean isErrorMessageDisplayed() {
        logger.info("Checking if error message is displayed");
        return isElementDisplayed(errorMessage);
    }

    public boolean isUsernameFieldDisplayed() {
        return isElementDisplayed(usernameField);
    }
}

