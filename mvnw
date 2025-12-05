#!/bin/sh
# Maven Wrapper script
set -e
MAVEN_WRAPPER_JAR=".mvn/wrapper/maven-wrapper.jar"
MAVEN_WRAPPER_PROPERTIES=".mvn/wrapper/maven-wrapper.properties"

# Download Maven if not present
if [ ! -f "$MAVEN_WRAPPER_JAR" ]; then
    echo "Maven Wrapper JAR not found. Please ensure .mvn/wrapper/maven-wrapper.jar exists."
    exit 1
fi

# Get distribution URL
if [ -f "$MAVEN_WRAPPER_PROPERTIES" ]; then
    DIST_URL=$(grep 'distributionUrl' "$MAVEN_WRAPPER_PROPERTIES" | cut -d'=' -f2-)
fi

MAVEN_HOME="${HOME}/.m2/wrapper/dists/apache-maven-3.9.6"

if [ ! -d "$MAVEN_HOME" ]; then
    echo "Downloading Maven..."
    mkdir -p "${HOME}/.m2/wrapper/dists"
    curl -sL "$DIST_URL" -o /tmp/maven.zip
    unzip -q /tmp/maven.zip -d "${HOME}/.m2/wrapper/dists"
    rm /tmp/maven.zip
fi

exec "$MAVEN_HOME/bin/mvn" "$@"

