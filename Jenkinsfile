pipeline {
    agent any
    environment {
        // Define DockerHub credentials ID
        DOCKERHUB_CREDENTIALS_ID = 'GilibeeDocker'
        // Define GitLab repository
        //GIT_REPO_URL = 'your_gitlab_project_url'
        // Docker image name
        IMAGE_NAME = 'gilibee/hailyeah'
        // Docker tag
        IMAGE_TAG = 'latest'
    }
    stages {
        stage('Checkout from GitLab') {
            steps {
                // Checkout code from GitLab
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                // Build Docker image using Docker Pipeline plugin
                script {
                    sh 'echo "starting dorker image build"'
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }
        stage('Run Pytest in Container') {
            steps {
                // Run a container from the image and execute pytest
                script {
        	    docker.image("${IMAGE_NAME}:${IMAGE_TAG}").run('--name hailyeah -d --rm -p 80:80')
                    dir('/home/jenkins/workspace/HailYeah_pipeline/API_Project') {
                        // run pytest retrypush2
                        sh 'pytest'        	    
                    }
                }
            }
        }
        stage('Push Image to DockerHub') {
            steps {
                script {
                    // Login and push to DockerHub using Docker Pipeline plugin
                    docker.withRegistry('https://index.docker.io', DOCKERHUB_CREDENTIALS_ID) {
                        docker.image("${IMAGE_NAME}:${IMAGE_TAG}").push("${IMAGE_TAG}")
                    }
                }
            }
        }
    }
   post {
        always {
            // Clean up Docker images
            script {
                sh 'docker kill ${IMAGE_NAME}'
            }
        }
    }
}
 
