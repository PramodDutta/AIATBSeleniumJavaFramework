package com.automation.tests;

import com.automation.base.BaseTest;
import com.automation.pages.DashboardPage;
import com.automation.pages.LoginPage;
import io.qameta.allure.*;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

@Epic("Login Feature")
@Feature("User Authentication")
public class LoginTest extends BaseTest {

        private LoginPage loginPage;

        // Test credentials for practice test automation site
        private static final String VALID_USERNAME = "student";
        private static final String VALID_PASSWORD = "Password123";
        private static final String INVALID_USERNAME = "invalidUser";
        private static final String INVALID_PASSWORD = "invalidPass";

        @BeforeMethod
        public void initLoginPage() {
                loginPage = new LoginPage(driver);
        }

        @Test(priority = 1, description = "Verify successful login with valid credentials")
        @Severity(SeverityLevel.CRITICAL)
        @Story("Valid Login")
        @Description("Test to verify that user can login successfully with valid username and password")
        public void testValidLogin() {
                logger.info("Starting valid login test");

                DashboardPage dashboardPage = loginPage.loginAs(VALID_USERNAME, VALID_PASSWORD);

                Assert.assertTrue(dashboardPage.isOnDashboardPage(),
                                "User should be redirected to dashboard after successful login");
                Assert.assertTrue(dashboardPage.isSuccessMessageDisplayed(),
                                "Success message should be displayed after login");
                Assert.assertTrue(dashboardPage.isLogoutButtonDisplayed(),
                                "Logout button should be visible on dashboard");

                logger.info("Valid login test completed successfully");
        }

        @Test(priority = 2, description = "Verify error message with invalid username")
        @Severity(SeverityLevel.NORMAL)
        @Story("Invalid Login")
        @Description("Test to verify that appropriate error message is displayed when invalid username is entered")
        public void testInvalidUsername() {
                logger.info("Starting invalid username test");

                loginPage.loginWithInvalidCredentials(INVALID_USERNAME, VALID_PASSWORD);

                Assert.assertTrue(loginPage.isErrorMessageDisplayed(),
                                "Error message should be displayed for invalid username");
                Assert.assertTrue(loginPage.getErrorMessage().contains("Your username is invalid"),
                                "Error message should indicate invalid username");

                logger.info("Invalid username test completed successfully");
        }

        @Test(priority = 3, description = "Verify error message with invalid password")
        @Severity(SeverityLevel.NORMAL)
        @Story("Invalid Login")
        @Description("Test to verify that appropriate error message is displayed when invalid password is entered")
        public void testInvalidPassword() {
                logger.info("Starting invalid password test");

                loginPage.loginWithInvalidCredentials(VALID_USERNAME, INVALID_PASSWORD);

                Assert.assertTrue(loginPage.isErrorMessageDisplayed(),
                                "Error message should be displayed for invalid password");
                Assert.assertTrue(loginPage.getErrorMessage().contains("Your password is invalid"),
                                "Error message should indicate invalid password");

                logger.info("Invalid password test completed successfully");
        }

        @Test(priority = 4, description = "Verify logout functionality")
        @Severity(SeverityLevel.CRITICAL)
        @Story("Logout")
        @Description("Test to verify that user can logout successfully from dashboard")
        public void testLogout() {
                logger.info("Starting logout test");

                DashboardPage dashboardPage = loginPage.loginAs(VALID_USERNAME, VALID_PASSWORD);
                Assert.assertTrue(dashboardPage.isOnDashboardPage(),
                                "User should be on dashboard page");

                LoginPage loginPageAfterLogout = dashboardPage.clickLogout();
                Assert.assertTrue(loginPageAfterLogout.isUsernameFieldDisplayed(),
                                "Username field should be displayed after logout");

                logger.info("Logout test completed successfully");
        }

        @Test(priority = 5, description = "Intentional failure test to verify screenshot capture")
        @Severity(SeverityLevel.MINOR)
        @Story("Screenshot Test")
        @Description("This test intentionally fails to verify that screenshot is captured on failure")
        public void testIntentionalFailureForScreenshot() {
                logger.info("Starting intentional failure test for screenshot verification");

                // Navigate and login first to have a meaningful screenshot
                DashboardPage dashboardPage = loginPage.loginAs(VALID_USERNAME, VALID_PASSWORD);
                Assert.assertTrue(dashboardPage.isOnDashboardPage(),
                                "User should be on dashboard page");

                // This assertion will intentionally FAIL to trigger screenshot capture
                Assert.assertEquals(driver.getTitle(), "This Title Does Not Exist - Intentional Failure",
                                "INTENTIONAL FAILURE: This test is designed to fail to verify screenshot capture works");
        }
}
