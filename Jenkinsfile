pipeline {
  agent any

  environment {
    IMAGE_NAME = 'princemitnick/ci-cd-tasks'
    DOCKERHUB_CREDENTIALS_ID = 'dockerhub-secrets'
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/princemitnick/ci-cd-testing.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          docker.build("${IMAGE_NAME}:latest")
        }
      }
    }

    stage('DockerHub Login') {
      steps {
        script {
          docker.withRegistry('https://index.docker.io/v1/', "${DOCKERHUB_CREDENTIALS_ID}") {
            echo "Logged in"
          }
        }
      }
    }

    stage('Push to DockerHub'){
      steps {
        script {
          docker.image("${IMAGE_NAME}:latest").push()
        }
      }
    }
  }
}

post {
  failure {
    echo "The build step failed"
  }
  success {
    echo "Build was successful"
  }
  always {
    echo "This run always."
  }
}