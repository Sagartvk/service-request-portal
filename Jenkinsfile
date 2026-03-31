pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-2'
        S3_BUCKET = 'sagar-service-request-portal-2026'
        SUBMIT_FUNCTION = 'submitRequestFunction'
        TRACK_FUNCTION = 'trackRequestFunction'
    }

    stages {

        stage('Checkout Code') {
            steps {
                git 'https://github.com/Sagartvk/service-request-portal.git'
            }
        }

        stage('Verify AWS CLI') {
            steps {
                sh 'aws --version'
            }
        }

        stage('Deploy Frontend to S3') {
            steps {
                sh '''
                aws s3 sync . s3://$S3_BUCKET \
                  --exclude ".git/*" \
                  --exclude "backend/*" \
                  --delete
                '''
            }
        }

        stage('Deploy Lambda - Submit') {
            steps {
                sh '''
                cd backend
                zip submit.zip submit_request.py

                aws lambda update-function-code \
                  --function-name $SUBMIT_FUNCTION \
                  --zip-file fileb://submit.zip \
                  --region $AWS_REGION
                '''
            }
        }

        stage('Deploy Lambda - Track') {
            steps {
                sh '''
                cd backend
                zip track.zip track_request.py

                aws lambda update-function-code \
                  --function-name $TRACK_FUNCTION \
                  --zip-file fileb://track.zip \
                  --region $AWS_REGION
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment Successful!'
        }
        failure {
            echo '❌ Deployment Failed!'
        }
    }
}
