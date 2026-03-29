pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning code...'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                cd /var/lib/jenkins/workspace/service-request-portal
                echo "Deploying app..."

                # Stop old process (ignore error)
                pkill -f submit_request.py || true

                # Run backend
                nohup python3 backend/submit_request.py > output.log 2>&1 &
                '''
            }
        }
    }
}
