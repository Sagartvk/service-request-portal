pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/Sagartvk/service-request-portal.git'
            }
        }

        stage('Build') {
            steps {
                echo "Build successful"
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploy step (static project)"
            }
        }
    }
}
