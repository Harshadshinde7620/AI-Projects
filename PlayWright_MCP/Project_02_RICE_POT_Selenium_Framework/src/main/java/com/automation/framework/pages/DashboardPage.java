package com.automation.framework.pages;

import com.automation.framework.base.DriverManager;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class DashboardPage {

    public DashboardPage() {
        PageFactory.initElements(DriverManager.getDriver(), this);
    }

    @FindBy(xpath = "//h6[contains(@class, 'oxd-topbar-header-breadcrumb-module')]")
    private WebElement dashboardHeader;

    public String getHeaderText() {
        return dashboardHeader.getText();
    }

    public boolean isDashboardDisplayed() {
        return dashboardHeader.isDisplayed();
    }
}
