pipeline {
    agent any

    environment {
        // Set environment variables if needed
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                // Clones the source code from your version control system (e.g., Git)
                checkout scm
            }
        }

        stage('Setup & Install Dependencies') {
            steps {
                // If your Jenkins server runs on Linux/Mac:
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    
                    # Uncomment the following line when you create a requirements.txt file
                    # pip install -r requirements.txt
                    
                    # Since there is no requirements.txt currently, installing django as an example
                    pip install django
                '''
                
                /*
                // If your Jenkins server runs on Windows, use 'bat' instead of 'sh':
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install django
                '''
                */
            }
        }

        stage('Run Tests') {
            steps {
                // Run your Django tests
                sh '''
                    . venv/bin/activate
                    python manage.py test
                '''
                
                /*
                // Windows equivalent:
                bat '''
                    call venv\\Scripts\\activate
                    python manage.py test
                '''
                */
            }
        }

        stage('Build Docker Image (Optional)') {
            // This stage will only run if a Dockerfile exists in your project
            when {
                expression { fileExists('Dockerfile') }
            }
            steps {
                echo "Dockerfile found! Building image..."
                // sh 'docker build -t my-django-app:latest .'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution complete.'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed. Check the logs.'
        }
    }
}
