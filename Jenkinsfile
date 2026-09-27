pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['DEV', 'UAT', 'PRODUCTION'],
            description: 'Select the environment to deploy'
        )
    }

    environment {
        IMAGE_NAME = 'customer-app'
        IMAGE_TAG = '1.0.0'
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                echo "Building Docker image..."
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% -f app/Dockerfile .'
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running application tests..."
                bat 'docker run --rm -v "%CD%:/workspace" -w /workspace %IMAGE_NAME%:%IMAGE_TAG% pytest tests'
            }
        }

        stage('Deploy Environment') {
            steps {
                script {

                    def serviceName

                    if (params.ENVIRONMENT == 'DEV') {
                        serviceName = 'customer-app-dev'
                    }
                    else if (params.ENVIRONMENT == 'UAT') {
                        serviceName = 'customer-app-uat'
                    }
                    else if (params.ENVIRONMENT == 'PRODUCTION') {
                        serviceName = 'customer-app-prod'
                    }
                    else {
                        error "Invalid environment selected: ${params.ENVIRONMENT}"
                    }

                    echo "Deploying to ${params.ENVIRONMENT}"
                    echo "Docker service: ${serviceName}"

                    bat "docker-compose up -d --force-recreate ${serviceName}"
                }
            }
        }

        stage('Validate Deployment') {
            steps {
                script {

                    def port

                    if (params.ENVIRONMENT == 'DEV') {
                        port = '8081'
                    }
                    else if (params.ENVIRONMENT == 'UAT') {
                        port = '8082'
                    }
                    else if (params.ENVIRONMENT == 'PRODUCTION') {
                        port = '8083'
                    }
                    else {
                        error "Invalid environment selected: ${params.ENVIRONMENT}"
                    }

                    echo "Validating ${params.ENVIRONMENT} deployment..."
                    echo "Application port: ${port}"

                    bat "curl --fail http://localhost:${port}/health"
                }
            }
        }
    }

    post {

        success {
            echo "=========================================="
            echo "Deployment Successful"
            echo "Environment: ${params.ENVIRONMENT}"
            echo "Version: ${IMAGE_TAG}"
            echo "=========================================="
        }

        failure {
            echo "=========================================="
            echo "Deployment Failed"
            echo "Environment: ${params.ENVIRONMENT}"
            echo "Check the Jenkins console log for details."
            echo "=========================================="
        }
    }
}