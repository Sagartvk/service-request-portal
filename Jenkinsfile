pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning code...'
            }
        }

        stage('Build') {
            steps {
                sh 'python3 --version || true'
                sh 'pip3 --version || true'
                echo 'Build stage running...'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy stage placeholder...'
            }
        }
    }
}
