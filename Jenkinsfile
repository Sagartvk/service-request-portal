pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning code...'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'sudo apt update'
                sh 'sudo apt install -y python3-pip'
                sh 'pip3 install -r backend/requirements.txt'
            }
        }

        stage('Run App (Test)') {
            steps {
                sh 'echo Running backend...'
            }
        }
    }
}
