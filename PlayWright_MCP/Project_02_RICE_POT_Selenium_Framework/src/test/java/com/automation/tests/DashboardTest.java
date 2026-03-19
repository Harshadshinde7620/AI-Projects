package com.automation.tests;

import com.automation.framework.base.BaseTest;
import com.automation.framework.pages.LoginPage;
import com.automation.framework.pages.DashboardPage;
import org.testng.Assert;
import org.testng.annotations.Test;

public class DashboardTest extends BaseTest {

    @Test(description = "Verify dashboard elements after login")
    public void testDashboardElements() {
        LoginPage loginPage = new LoginPage();
        loginPage.login("Admin", "admin123");

        DashboardPage dashboardPage = new DashboardPage();
        Assert.assertTrue(dashboardPage.isDashboardDisplayed(), "Dashboard should be visible");
        Assert.assertEquals(dashboardPage.getHeaderText(), "Dashboard", "Dashboard header should be present");
    }
}
