pipeline {
    agent any
    environment {
        // Define DockerHub credentials ID
        DOCKERHUB_CREDENTIALS_ID = 'GilibeeDocker'
        // Define GitLab repository
        //GIT_REPO_URL = 'your_gitlab_project_url'
        // Docker image name
        IMAGE_NAME = 'hailyeah'
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
                    // retry3
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
        	    docker.image('IMAGE_NAME:IMAGE_TAG').run('--name hailyeah -d -p 80:80')
                }
            }
        }
    }
}
 
