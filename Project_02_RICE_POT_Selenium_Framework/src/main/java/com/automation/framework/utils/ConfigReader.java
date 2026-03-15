package com.automation.framework.utils;

import com.automation.framework.constants.FrameworkConstants;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public final class ConfigReader {

    private static Properties properties = new Properties();

    static {
        try (FileInputStream fis = new FileInputStream(FrameworkConstants.getConfigFilePath())) {
            properties.load(fis);
        } catch (IOException e) {
            throw new RuntimeException("Could not load config file at " + FrameworkConstants.getConfigFilePath());
        }
    }

    public static String getProperty(String key) {
        return properties.getProperty(key);
    }
}
