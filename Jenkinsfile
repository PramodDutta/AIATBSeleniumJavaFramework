pipeline {
    agent any

    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox', 'edge'],
            description: 'Browser to run tests'
        )
        choice(
            name: 'EXECUTION_ENV',
            choices: ['local', 'browserstack', 'lambdatest'],
            description: 'Test execution environment'
        )
        string(
            name: 'TEST_SUITE',
            defaultValue: 'testng.xml',
            description: 'TestNG suite file to execute'
        )
        booleanParam(
            name: 'GENERATE_AI_REPORT',
            defaultValue: true,
            description: 'Generate AI analysis report'
        )
    }

    environment {
        // BrowserStack credentials (set in Jenkins credentials)
        BROWSERSTACK_USERNAME = credentials('browserstack-username')
        BROWSERSTACK_ACCESS_KEY = credentials('browserstack-access-key')
        
        // LambdaTest credentials (set in Jenkins credentials)
        LAMBDATEST_USERNAME = credentials('lambdatest-username')
        LAMBDATEST_ACCESS_KEY = credentials('lambdatest-access-key')
        
        // Java & Maven
        JAVA_HOME = tool 'JDK17'
        MAVEN_HOME = tool 'Maven3'
        PATH = "${JAVA_HOME}/bin:${MAVEN_HOME}/bin:${PATH}"
    }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Branch: ${env.BRANCH_NAME ?: 'main'}"
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    echo "Java Version:"
                    java -version
                    echo "Maven Version:"
                    mvn -version
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean compile -DskipTests'
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def mvnCommand = """
                        mvn test \
                        -Dbrowser=${params.BROWSER} \
                        -Dexecution.env=${params.EXECUTION_ENV} \
                        -DsuiteXmlFile=${params.TEST_SUITE} \
                        -Dbrowserstack.username=${BROWSERSTACK_USERNAME} \
                        -Dbrowserstack.accessKey=${BROWSERSTACK_ACCESS_KEY} \
                        -Dlambdatest.username=${LAMBDATEST_USERNAME} \
                        -Dlambdatest.accessKey=${LAMBDATEST_ACCESS_KEY}
                    """
                    sh mvnCommand
                }
            }
            post {
                always {
                    // Archive test results
                    junit allowEmptyResults: true, testResults: '**/target/surefire-reports/*.xml'
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'target/allure-results']]
                ])
            }
        }

        stage('AI Analysis') {
            when {
                expression { params.GENERATE_AI_REPORT == true }
            }
            steps {
                script {
                    sh '''
                        cd ai-analysis
                        python3 -m venv venv || true
                        . venv/bin/activate
                        pip install -r requirements.txt --quiet
                        python report_generator.py -o ../target/ai-report.html
                    '''
                }
            }
            post {
                success {
                    archiveArtifacts artifacts: 'target/ai-report.html', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed'
            cleanWs()
        }
        success {
            echo '✅ Tests passed successfully!'
        }
        failure {
            echo '❌ Tests failed! Check the reports for details.'
        }
    }
}

