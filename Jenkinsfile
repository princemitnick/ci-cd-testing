pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS_ID = 'dockerhub-secrets'
    DOCKERHUB_USERNAME = 'princemintnick'
    IMAGE_REPO = 'fast-api-ci-cd'
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/princemitnick/ci-cd-testing.git'
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS_ID}", usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
          script {
            def commitHash = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
            def imageName = "${DOCKERHUB_USERNAME}/${IMAGE_REPO}"
            def tagLatest = "${imageName}:latest"
            def tagCommit = "${imageName}:${commitHash}"

            echo "Building Docker image with tags: latest and ${commitHash}"

            // Login to Docker Hub
            sh "echo $PASSWORD | docker login -u $USER --password-stdin"

            // Build and tag
            sh "docker build -t ${tagLatest} ."
            sh "docker tag ${tagLatest} ${tagCommit}"

            // Push both tags
            sh "docker push ${tagLatest}"
            sh "docker push ${tagCommit}"
          }
        }
      }
    }
  }

  post {
    success {
      echo "✅ Build and push completed successfully"
    }
    failure {
      echo "❌ Build or push failed"
    }
    always {
      echo "📦 Pipeline finished"
    }
  }
}