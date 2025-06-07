pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS_ID = ''
    DOCKERHUB_USERNAME = 'princemitnick'
    IMAGE_REPO = 'fast-api-ci-cd'
  }

  options {
    timestamps()
  }

  stages {
    stage('Checkout Code') {
      steps {
        git branch: 'main', url: 'https://github.com/princemitnick/ci-cd-testing'
      }
    }

    stage('Prepare Tags') {
      steps {
        script {
          COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
          BUILD_TAG = "${COMMIT_HASH}-${env.BUILD_NUMBER}"
          IMAGE_NAME = "${DOCKERHUB_USERNAME}/$IMAGE_REPO"
          TAG_LATEST = "${IMAGE_NAME}:latest"
          TAG_BUILD = "${IMAGE_NAME}:${BUILD_TAG}"

          echo "Tags préparés : "
          echo "   - ${TAG_LATEST}"
          echo "   - ${TAG_BUILD}"
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          sh "docker build -t ${TAG_LATEST} ."
          sh "docker tag ${TAG_LATEST} ${TAG_BUILD}"
        }
      }
    }

    stage('Security Scan') {
      steps {
        script {
          echo "Scan de sécurité avec Trivy..."
          sh "trivy image ${TAG_BUILD} || true"
        }
      }
    }

    stage('Test Docker Image') {
      steps {
        script {
          echo "Lancement temporaire de l'image pour test..."
          sh "docker run -d --name fastapi_test -p 8000:8000 ${TAG_BUILD}"

          sleep time: 5, unit: 'SECOND'

          echo "Test de l'endpoint /health ou /"
          def status = sh(script: "curl -s -o /dev/null -w '%http_code' http://localhost:8000/", returnStdout: true).trim()

          sh "docker stop fastapi_test"
          sh "docker rm fastapi_test"

          if (status != '200') {
            error("L'image ne répond pas correctement. Code HTTP : ${status}")
          } else {
            echo "L'image a répondu correctement avec HTTP ${status}"
          }
        }
      }
    }

    stage('Push to DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS_ID}", usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
          script {
            sh "echo $PASSWORD | docker login -u $USER --password-stdin ${DOCKER_REGISTRY}"
            sh "docker push ${TAG_BUILD}"
            sh "docker push $TAG_LATEST"
          }
        }
      }
    }

    stage('Cleanup Local Images'){
      steps {
        script {
          steps {
            script {
              echo "Supression des images locales pour garder le workspace propre"
              sh "docker rmi ${TAG_BUILD} ${TAG_LATEST} || true"
            }
          }
        }
      }
    }
  }

  post {
    success {
      echo "Pipeline terminé avec succès !"
    }
    failure {
      echo "Pipeline échoué. Voir les logs pour détails."
    }
    always {
      echo "Fin d'execution pipeline."
    }
  }
}