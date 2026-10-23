

pipeline {
    agent any

    stages {
        stage('Check Docker') {
            steps {
                bat 'docker --version'
                bat 'docker info'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t my-dashboard-app .'
            }
        }

        stage('Django System Check') {
            steps {
                bat 'docker run --rm my-dashboard-app python manage.py check'
            }
        }

        stage('Deploy Dashboard') {
            steps {
                bat '''
                    docker rm -f model-dashboard 2>NUL
                    docker run -d --restart unless-stopped --name model-dashboard -p 8002:8000 -e DB_PATH=/data/db.sqlite3 -v model-dashboard-data:/data my-dashboard-app
                    if errorlevel 1 exit /b 1

                    powershell -NoProfile -Command "Start-Sleep -Seconds 5"

                    docker inspect -f "{{.State.Running}}" model-dashboard | findstr /x "true"
if errorlevel 1 exit /b 1
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD successful! Dashboard deployed.'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
