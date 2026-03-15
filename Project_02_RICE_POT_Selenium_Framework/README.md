# Selenium Automation Framework

A production-ready Selenium Automation Framework built with Java, TestNG, and Maven, following the Page Object Model (POM) pattern.

## Features

- **Language**: Java
- **Browser Automation**: Selenium 4
- **Test Runner**: TestNG
- **Dependency Management**: Maven
- **Driver Management**: WebDriverManager
- **Design Pattern**: Page Object Model (POM) with PageFactory
- **Reporting**: Extent Reports (Integrated via BaseTest/Listeners)
- **Logging**: Log4j 2
- **Data Management**: Externalized configuration (config.properties) and Test Data (JSON)
- **Parallel Execution**: Supported via TestNG (configured in `testng.xml`)
- **Error Handling**: Automatic screenshot capture on failure

## Project Structure

```
project_02_SeleniumFramework
├── pom.xml
├── testng.xml
├── README.md
├── src
│   ├── main
│   │   └── java/com/automation/framework
│   │       ├── base/DriverManager, BaseTest
│   │       ├── pages/LoginPage, DashboardPage
│   │       ├── factory/BrowserFactory
│   │       ├── utils/WaitUtils, ScreenshotUtils, ConfigReader, JsonUtils
│   │       └── constants/FrameworkConstants
│   └── test
│       ├── java/com/automation/tests/LoginTest, InvalidLoginTest, DashboardTest
│       └── resources/config.properties, testdata.json, log4j2.xml
├── reports/ (Created at runtime)
├── screenshots/ (Created at runtime)
└── logs/ (Created at runtime)
```

## Setup and Execution

1. **Prerequisites**:
   - JDK 11 or higher
   - Maven installed

2. **Configuration**:
   - Update `src/test/resources/config.properties` for URL and browser preferences.

3. **Running Tests**:
   - Run from command line: `mvn test`
   - Run via TestNG: Right-click `testng.xml` and select "Run".

4. **Viewing Reports**:
   - After execution, open `reports/index.html` in any browser.

## Best Practices Followed
- ThreadLocal WebDriver for safe parallel execution.
- Explicit waits to avoid flaky tests.
- Reusable utilities for common actions.
- Separation of concerns (Logic, Pages, Tests).
