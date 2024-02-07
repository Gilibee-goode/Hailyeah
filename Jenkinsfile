pipeline {
    agent any
    environment {
        // Define DockerHub credentials ID
        DOCKERHUB_CREDENTIALS_ID = 'GilibeeDocker'
        // Docker image name
        IMAGE_NAME = 'gilibee/hailyeah'
        // Docker tag
        IMAGE_TAG = 'latest'
        // Deploy location (Hailyeah server) FFS
        DEPLOY_IP = '13.49.145.240'
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
	stage('Deploy to AWS - sh') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'aws-ssh-ubuntu', keyFileVariable: 'SSH_PRIVATE_KEY')]) {
                    script {
                        sh "ssh-keyscan -H ${DEPLOY_IP} >> ~/.ssh/known_hosts"
                        //docker.image("${IMAGE_NAME}:${IMAGE_TAG}").run('--name hailyeah -d --rm -p 80:80')
                        //sh "ssh -i ${SSH_PRIVATE_KEY} ubuntu@${DEPLOY_IP} docker pull bensh99/simpleapp:latest"
                        sh "ssh -i ${SSH_PRIVATE_KEY} ubuntu@${DEPLOY_IP} docker pull ${IMAGE_NAME}:${IMAGE_TAG}"
                        sh "ssh -i ${SSH_PRIVATE_KEY} ubuntu@${DEPLOY_IP} docker kill hailyeah"
                        sh "ssh -i ${SSH_PRIVATE_KEY} ubuntu@${DEPLOY_IP} docker container prune -f"
                        sh "ssh -i ${SSH_PRIVATE_KEY} ubuntu@${DEPLOY_IP} docker run --rm --name hailyeah -p 80:80 -d ${IMAGE_NAME}:${IMAGE_TAG}"
                    }
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
 
