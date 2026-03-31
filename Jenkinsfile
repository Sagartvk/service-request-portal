pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-2"   // change if needed
        S3_BUCKET = "sagar-service-request-portal-2026"  // 🔥 your bucket name
        LAMBDA_SUBMIT = "submitRequestFunction"
        LAMBDA_TRACK = "trackRequestFunction"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Sagartvk/service-request-portal.git'
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
                --exclude "lambda/*"
                '''
            }
        }

        stage('Deploy Lambda - Submit') {
            steps {
                sh '''
                cd lambda
                zip -r submit.zip submit.py
                aws lambda update-function-code \
                --function-name $LAMBDA_SUBMIT \
                --zip-file fileb://submit.zip \
                --region $AWS_REGION
                '''
            }
        }

        stage('Deploy Lambda - Track') {
            steps {
                sh '''
                cd lambda
                zip -r track.zip track.py
                aws lambda update-function-code \
                --function-name $LAMBDA_TRACK \
                --zip-file fileb://track.zip \
                --region $AWS_REGION
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployment Successful!"
        }
        failure {
            echo "❌ Deployment Failed!"
        }
    }
}
