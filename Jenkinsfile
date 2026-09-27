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
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% -f app/Dockerfile .'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'docker run --rm -v "%CD%:/workspace" -w /workspace %IMAGE_NAME%:%IMAGE_TAG% pytest tests'
            }
        }

        stage('Deploy Environment') {
            steps {
                script {
                    def serviceName = ''

                    if (params.ENVIRONMENT == 'DEV') {
                        serviceName = 'customer-app-dev'
                    } else if (params.ENVIRONMENT == 'UAT') {
                        serviceName = 'customer-app-uat'
                    } else {
                        serviceName = 'customer-app-prod'
                    }

                    bat "docker compose up -d --force-recreate ${serviceName}"
                }
            }
        }

        stage('Validate Deployment') {
            steps {
                script {
                    def port = ''

                    if (params.ENVIRONMENT == 'DEV') {
                        port = '8081'
                    } else if (params.ENVIRONMENT == 'UAT') {
                        port = '8082'
                    } else {
                        port = '8083'
                    }

                    bat "curl --fail http://localhost:${port}/health"
                }
            }
        }
    }

    post {
        success {
            echo "Deployment to ${params.ENVIRONMENT} completed successfully."
        }

        failure {
            echo "Deployment to ${params.ENVIRONMENT} failed."
        }
    }
}