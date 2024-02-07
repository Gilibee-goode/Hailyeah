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
        // Deploy location
        DEPLOY_IP = 13.49.145.240
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
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS_ID) {
                        docker.image("${IMAGE_NAME}:${IMAGE_TAG}").push("${IMAGE_TAG}")
                    }
                }
            }
        }
        stage('Deploy to AWS') {
            steps {
                script {
                    // Define remote server SSH connection
                    def remote = [:]
                    remote.name = "ubuntu"
                    remote.host = ${DEPLOY_IP}
                    remote.user = "ubuntu"
                    remote.credentialsId = "aws-ssh-ubuntu"
                    remote.allowAnyHosts = true 

                    // Commands to pull and run your Docker container
                    def deployCommands = """
                        docker pull ${IMAGE_NAME}:${IMAGE_TAG} && \
                        docker stop hailyeah || true && \
                        docker run --name hailyeah -d ${IMAGE_NAME}:${IMAGE_TAG}
                    """

                    // Execute commands on the remote server
                    sshCommand remote: remote, command: deployCommands
                }
            }
        }
    }
   post {
        always {
            // Clean up Docker images
            script {
                sh 'docker kill hailyeah'
            }
        }
    }
}
 
