pipeline {
    agent any

    environment {
        IMAGE = 'pranathidevaki/devops_week12:latest'
        BASE_URL = 'http://localhost:30120/'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                bat "docker build -t %IMAGE% ."
            }
        }
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS%| docker login -u %DOCKER_USER% --password-stdin'
                }
            }
        }
        stage('Push Docker Image to Docker Hub') {
            steps {
                bat "docker push %IMAGE%"
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
                // replace the old pod so the new image is used, then wait until it is Ready
                bat 'kubectl delete pod -l app=week12app'
                bat 'kubectl wait --for=condition=Ready pod -l app=week12app --timeout=120s'
            }
        }
        stage('Run Selenium Tests with pytest') {
            steps {
                echo 'Testing the app running on Kubernetes (port 30120)'
                bat 'python -m pip install -r requirements.txt'
                // forward localhost:30120 to the service, wait, then run the tests
                bat '''
                    start /B kubectl port-forward service/week12app-service 30120:5000
                    ping 127.0.0.1 -n 6 > nul
                    python -m pytest -v tests
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
