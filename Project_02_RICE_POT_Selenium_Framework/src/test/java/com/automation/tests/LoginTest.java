package com.automation.tests;

import com.automation.framework.base.BaseTest;
import com.automation.framework.pages.LoginPage;
import com.automation.framework.pages.DashboardPage;
import org.testng.Assert;
import org.testng.annotations.Test;

public class LoginTest extends BaseTest {

    @Test(description = "Verify successful login with valid credentials")
    public void testSuccessfulLogin() {
        LoginPage loginPage = new LoginPage();
        loginPage.login("Admin", "admin123");

        DashboardPage dashboardPage = new DashboardPage();
        Assert.assertTrue(dashboardPage.isDashboardDisplayed(), "Dashboard should be displayed after login");
        Assert.assertEquals(dashboardPage.getHeaderText(), "Dashboard", "Header text should be correct");
    }
}
