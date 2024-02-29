pipeline {
    agent any


    stages {
        stage('Build Image') {
            steps {
                echo '==============build version============='
                sh 'docker compose up -d --build'
            }
        }
    }
}