package com.automation.framework.utils;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.automation.framework.constants.FrameworkConstants;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;

public final class JsonUtils {

    private JsonUtils() {}

    public static List<Map<String, String>> getTestData() {
        ObjectMapper mapper = new ObjectMapper();
        try {
            return mapper.readValue(new File(FrameworkConstants.getTestDataJsonPath()), 
                new TypeReference<List<Map<String, String>>>() {});
        } catch (IOException e) {
            throw new RuntimeException("Failed to read test data from " + FrameworkConstants.getTestDataJsonPath());
        }
    }
}
