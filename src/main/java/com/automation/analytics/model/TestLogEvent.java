package com.automation.analytics.model;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Structured log event model for AI-powered test analysis.
 * Compatible with LogAI pipeline and OpenTelemetry format.
 */
public class TestLogEvent {

    private String eventId;
    private String timestamp;
    private String testId;
    private String testName;
    private String suite;
    private String className;
    private String environment;
    private String level;  // INFO, WARN, ERROR, FATAL
    private String status; // PASSED, FAILED, SKIPPED
    private String message;
    private String stacktrace;
    private String service;
    private long durationMs;
    private Map<String, String> attributes;

    public TestLogEvent() {
        this.eventId = UUID.randomUUID().toString();
        this.timestamp = Instant.now().toString();
        this.attributes = new HashMap<>();
    }

    // Builder pattern for fluent API
    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private final TestLogEvent event;

        public Builder() {
            this.event = new TestLogEvent();
        }

        public Builder testId(String testId) {
            event.testId = testId;
            return this;
        }

        public Builder testName(String testName) {
            event.testName = testName;
            return this;
        }

        public Builder suite(String suite) {
            event.suite = suite;
            return this;
        }

        public Builder className(String className) {
            event.className = className;
            return this;
        }

        public Builder environment(String environment) {
            event.environment = environment;
            return this;
        }

        public Builder level(String level) {
            event.level = level;
            return this;
        }

        public Builder status(String status) {
            event.status = status;
            return this;
        }

        public Builder message(String message) {
            event.message = message;
            return this;
        }

        public Builder stacktrace(String stacktrace) {
            event.stacktrace = stacktrace;
            return this;
        }

        public Builder service(String service) {
            event.service = service;
            return this;
        }

        public Builder durationMs(long durationMs) {
            event.durationMs = durationMs;
            return this;
        }

        public Builder attribute(String key, String value) {
            event.attributes.put(key, value);
            return this;
        }

        public Builder attributes(Map<String, String> attributes) {
            event.attributes.putAll(attributes);
            return this;
        }

        public TestLogEvent build() {
            return event;
        }
    }

    // Getters
    public String getEventId() { return eventId; }
    public String getTimestamp() { return timestamp; }
    public String getTestId() { return testId; }
    public String getTestName() { return testName; }
    public String getSuite() { return suite; }
    public String getClassName() { return className; }
    public String getEnvironment() { return environment; }
    public String getLevel() { return level; }
    public String getStatus() { return status; }
    public String getMessage() { return message; }
    public String getStacktrace() { return stacktrace; }
    public String getService() { return service; }
    public long getDurationMs() { return durationMs; }
    public Map<String, String> getAttributes() { return attributes; }
}

