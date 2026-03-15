package com.automation.tests;

import com.automation.framework.base.BaseTest;
import com.automation.framework.pages.LoginPage;
import org.testng.Assert;
import org.testng.annotations.Test;

public class InvalidLoginTest extends BaseTest {

    @Test(description = "Verify error message with invalid credentials")
    public void testInvalidLogin() {
        LoginPage loginPage = new LoginPage();
        loginPage.login("InvalidUser", "InvalidPass");

        String actualError = loginPage.getErrorMessage();
        Assert.assertEquals(actualError, "Invalid credentials", "Error message should match");
    }
}
