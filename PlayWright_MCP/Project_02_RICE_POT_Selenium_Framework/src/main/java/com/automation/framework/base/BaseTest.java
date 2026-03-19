package com.automation.framework.base;

import com.automation.framework.factory.BrowserFactory;
import com.automation.framework.utils.ConfigReader;
import com.automation.framework.utils.ScreenshotUtils;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Optional;
import org.testng.annotations.Parameters;
import java.time.Duration;

public class BaseTest {

    @BeforeMethod
    @Parameters("browser")
    public void setup(@Optional("chrome") String browser) {
        String browserName = (browser != null) ? browser : ConfigReader.getProperty("browser");
        WebDriver driver = BrowserFactory.createDriver(browserName);
        DriverManager.setDriver(driver);
        DriverManager.getDriver().manage().window().maximize();
        DriverManager.getDriver().manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        DriverManager.getDriver().get(ConfigReader.getProperty("url"));
    }

    @AfterMethod
    public void tearDown(ITestResult result) {
        if (result.getStatus() == ITestResult.FAILURE) {
            ScreenshotUtils.captureScreenshot(DriverManager.getDriver(), result.getName());
        }
        if (DriverManager.getDriver() != null) {
            DriverManager.getDriver().quit();
            DriverManager.unloadDriver();
        }
    }
}
