package com.automation.framework.constants;

public final class FrameworkConstants {

    private FrameworkConstants() {}

    private static final String RESOURCES_PATH = System.getProperty("user.dir") + "/src/test/resources";
    private static final String CONFIG_FILE_PATH = RESOURCES_PATH + "/config.properties";
    private static final String TEST_DATA_JSON_PATH = RESOURCES_PATH + "/testdata.json";
    private static final String EXTENT_REPORT_PATH = System.getProperty("user.dir") + "/reports/index.html";
    private static final String SCREENSHOT_PATH = System.getProperty("user.dir") + "/screenshots";

    public static String getConfigFilePath() {
        return CONFIG_FILE_PATH;
    }

    public static String getTestDataJsonPath() {
        return TEST_DATA_JSON_PATH;
    }

    public static String getExtentReportPath() {
        return EXTENT_REPORT_PATH;
    }

    public static String getScreenshotPath() {
        return SCREENSHOT_PATH;
    }
}
