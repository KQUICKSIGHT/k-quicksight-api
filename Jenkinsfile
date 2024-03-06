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

 post {
            success {
                sh """
                curl -s -X POST https://api.telegram.org/bot7082427729:AAElAcSJXbrLXTupwFlja_k_ukBbt7lp9Aw/sendMessage -d chat_id=-4110018997 -d text='
                    🎉 *Deployment Success API* 🎉
Project: K-QUICKSIGHT
Environment: STAGE
Version: 1.0.0
URL: http://34.101.151.18:8083/
Deployed By: CHEA CHENTO

Check out the latest version in action!
                '
                """
            }
            failure {
                sh """
                curl -s -X POST https://api.telegram.org/bot7082427729:AAElAcSJXbrLXTupwFlja_k_ukBbt7lp9Aw/sendMessage -d chat_id=-4110018997 -d text='
                    ⚠️ *Deployment Failure API* ⚠️
Project: K-QUICKSIGHT
Environment: STAGE
Version: 1.0.0
URL: http://34.101.151.18:8083/
Attempted By: CHEA CHENTO

Please check the logs and take the necessary action. Contact the team if the issue persists.
                '
                """
            }
        }

}
