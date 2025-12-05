package com.automation.analytics;

import com.automation.analytics.model.TestLogEvent;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

/**
 * Logger service that emits structured JSON logs for AI analysis pipeline.
 * Outputs JSONL format compatible with LogAI and OpenTelemetry collectors.
 */
public class TestAnalyticsLogger {

    private static final Logger logger = LogManager.getLogger(TestAnalyticsLogger.class);
    private static final String DEFAULT_LOG_DIR = "target/analytics-logs";
    private static final String LOG_FILE_NAME = "test-events.jsonl";

    private static TestAnalyticsLogger instance;
    private final Gson gson;
    private final Path logFilePath;
    private final String environment;
    private final String serviceName;

    private TestAnalyticsLogger() {
        this.gson = new GsonBuilder()
                .disableHtmlEscaping()
                .create();
        this.environment = System.getProperty("test.environment", "local");
        this.serviceName = System.getProperty("test.service", "selenium-ui-tests");
        this.logFilePath = initLogFile();
    }

    public static synchronized TestAnalyticsLogger getInstance() {
        if (instance == null) {
            instance = new TestAnalyticsLogger();
        }
        return instance;
    }

    private Path initLogFile() {
        try {
            Path logDir = Paths.get(DEFAULT_LOG_DIR);
            Files.createDirectories(logDir);
            Path filePath = logDir.resolve(LOG_FILE_NAME);
            logger.info("Analytics log file initialized at: " + filePath.toAbsolutePath());
            return filePath;
        } catch (IOException e) {
            logger.error("Failed to initialize analytics log directory", e);
            throw new RuntimeException("Cannot initialize analytics logging", e);
        }
    }

    /**
     * Log a test event in JSONL format for AI analysis pipeline.
     */
    public void logEvent(TestLogEvent event) {
        String jsonLine = gson.toJson(event);
        writeToFile(jsonLine);

        // Also log to standard logger for immediate visibility
        if ("ERROR".equals(event.getLevel()) || "FAILED".equals(event.getStatus())) {
            logger.error("[ANALYTICS] " + jsonLine);
        } else {
            logger.info("[ANALYTICS] " + jsonLine);
        }
    }

    /**
     * Log test start event.
     */
    public void logTestStart(String testId, String testName, String suite, String className) {
        TestLogEvent event = TestLogEvent.builder()
                .testId(testId)
                .testName(testName)
                .suite(suite)
                .className(className)
                .environment(environment)
                .service(serviceName)
                .level("INFO")
                .status("STARTED")
                .message("Test execution started")
                .build();
        logEvent(event);
    }

    /**
     * Log test success event.
     */
    public void logTestSuccess(String testId, String testName, String suite,
            String className, long durationMs) {
        TestLogEvent event = TestLogEvent.builder()
                .testId(testId)
                .testName(testName)
                .suite(suite)
                .className(className)
                .environment(environment)
                .service(serviceName)
                .level("INFO")
                .status("PASSED")
                .message("Test passed successfully")
                .durationMs(durationMs)
                .build();
        logEvent(event);
    }

    /**
     * Log test failure event with stacktrace for AI analysis.
     */
    public void logTestFailure(String testId, String testName, String suite,
            String className, long durationMs,
            String errorMessage, String stacktrace) {
        TestLogEvent event = TestLogEvent.builder()
                .testId(testId)
                .testName(testName)
                .suite(suite)
                .className(className)
                .environment(environment)
                .service(serviceName)
                .level("ERROR")
                .status("FAILED")
                .message(errorMessage)
                .stacktrace(stacktrace)
                .durationMs(durationMs)
                .build();
        logEvent(event);
    }

    /**
     * Log test skip event.
     */
    public void logTestSkipped(String testId, String testName, String suite,
            String className, String reason) {
        TestLogEvent event = TestLogEvent.builder()
                .testId(testId)
                .testName(testName)
                .suite(suite)
                .className(className)
                .environment(environment)
                .service(serviceName)
                .level("WARN")
                .status("SKIPPED")
                .message(reason != null ? reason : "Test skipped")
                .build();
        logEvent(event);
    }

    private synchronized void writeToFile(String jsonLine) {
        try {
            Files.writeString(logFilePath, jsonLine + System.lineSeparator(),
                    StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        } catch (IOException e) {
            logger.error("Failed to write analytics log", e);
        }
    }

    public Path getLogFilePath() {
        return logFilePath;
    }
}
