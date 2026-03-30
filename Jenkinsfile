pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '-u root'
        }
    }

    environment {
        AWS_DEFAULT_REGION = 'us-east-2'
    }

    stages {

        stage('Install Tools') {
            steps {
                sh '''
                apt-get update
                apt-get install -y zip curl unzip
                pip install awscli boto3
                '''
            }
        }

        stage('Deploy Frontend to S3') {
            steps {
                sh '''
                aws s3 sync frontend/ s3://sagar-service-request-portal-2026 --delete
                '''
            }
        }

        stage('Package Submit Lambda') {
            steps {
                sh '''
                cd backend
                zip -j submit_request.zip submit_request.py
                '''
            }
        }

        stage('Deploy Submit Lambda') {
            steps {
                sh '''
                aws lambda update-function-code \
                --function-name submitRequestFunction \
                --zip-file fileb://backend/submit_request.zip
                '''
            }
        }

        stage('Package Track Lambda') {
            steps {
                sh '''
                cd backend
                zip -j track_request.zip track_request.py
                '''
            }
        }

        stage('Deploy Track Lambda') {
            steps {
                sh '''
                aws lambda update-function-code \
                --function-name trackRequestFunction \
                --zip-file fileb://backend/track_request.zip
                '''
            }
        }
    }
}
