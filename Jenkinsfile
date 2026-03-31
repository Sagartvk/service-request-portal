pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-2'
        S3_BUCKET = 'sagar-service-request-portal-2026'
        CLOUDFRONT_DISTRIBUTION_ID = 'E22CABI5YY6I6F'
        SUBMIT_LAMBDA = 'submitRequestFunction'
        TRACK_LAMBDA = 'trackRequestFunction'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Using code from GitHub'
            }
        }

        stage('Deploy Frontend to S3') {
            steps {
                sh '''
                    aws s3 sync frontend/ s3://$S3_BUCKET --delete --region $AWS_REGION
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
                      --function-name $SUBMIT_LAMBDA \
                      --zip-file fileb://backend/submit_request.zip \
                      --region $AWS_REGION
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
                      --function-name $TRACK_LAMBDA \
                      --zip-file fileb://backend/track_request.zip \
                      --region $AWS_REGION
                '''
            }
        }

        stage('Invalidate CloudFront Cache') {
            steps {
                sh '''
                    aws cloudfront create-invalidation \
                      --distribution-id $CLOUDFRONT_DISTRIBUTION_ID \
                      --paths "/*"
                '''
            }
        }
    }
}
