pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS_ID = 'dockerhub-secrets'
    DOCKERHUB_USERNAME = 'princemitnick'
    IMAGE_REPO = 'fastapi-ci-cd'
    DOCKER_REGISTRY = 'https://index.docker.io/v1/'
  }

  options {
    timestamps()
  }

  stages {
    stage('Checkout Code') {
      steps {
        git branch: 'main', url: 'https://github.com/princemitnick/ci-cd-testing.git'
      }
    }

    stage('Prepare Tags') {

      steps {
        script {
          COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
          BUILD_TAG = "${COMMIT_HASH}-${env.BUILD_NUMBER}"
          IMAGE_NAME = "${DOCKERHUB_USERNAME}/${IMAGE_REPO}"
          TAG_LATEST = "${IMAGE_NAME}:latest"
          TAG_BUILD = "${IMAGE_NAME}:${BUILD_TAG}"
          echo "➡️ Tags: ${TAG_LATEST}, ${TAG_BUILD}"
        }
      }
    }

    stage('Build Multi-Arch Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS_ID}", usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
          script {
            sh """
              docker login -u $USER -p $PASSWORD ${DOCKER_REGISTRY}
              docker buildx create --use --name multiarch-builder || true
              docker buildx build --platform linux/amd64,linux/arm64 \
                -t ${TAG_LATEST} -t ${TAG_BUILD} \
                --push .
            """
          }
        }
      }
    }

    stage('Security Scan') {
      steps {
        script {
          echo "🔍 Scan de sécurité avec Trivy..."
          sh "trivy image ${TAG_BUILD} || true"
        }
      }
    }

    /*stage('Test Docker Image') {
      steps {
        script {
          sh "docker run -d --name fastapi_test -p 8000:8000 ${TAG_BUILD}"
          sleep time: 5, unit: 'SECONDS'
          def status = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/", returnStdout: true).trim()
          sh "docker stop fastapi_test"
          sh "docker rm fastapi_test"
          if (status != '200') {
            error("L’image ne répond pas correctement. HTTP ${status}")
          }
        }
      }
    }*/

    stage('Git Tag & Push') {
      steps {
        script {
          def version = "v1.0.${env.BUILD_NUMBER}"
          sh "git config user.name 'jenkins'"
          sh "git config user.email 'jenkins@ci.local'"
          sh "git tag ${version}"
          sh "git push origin ${version}"
        }
      }
    }

    stage('Deploy to Remote Server') {
      steps {
        sshagent(credentials: ['my-ssh-server-key']) {
          sh '''
            ssh -o StrictHostKeyChecking=no test@192.168.58.108 <<EOF
            docker pull ${TAG_BUILD}
            docker stop fastapi-app || true
            docker rm fastapi-app || true
            docker run -d --name fastapi-app -p 80:8000 ${TAG_BUILD}
            EOF
          '''
        }
      }
    }

    stage('Cleanup') {
      steps {
        script {
          echo "Nettoyage local..."
          sh "docker rmi ${TAG_BUILD} ${TAG_LATEST} || true"
        }
      }
    }
  }

  post {
    success {
      echo "Pipeline terminé avec succès !"
    }
    failure {
      echo "Échec du pipeline. Consulte les logs."
    }
    always {
      echo "Fin de l’exécution du pipeline."
    }
  }
}
