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
    skipDefaultCheckout(true)
  }

  stages {
    stage('Checkout Code') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/main']],
          userRemoteConfigs: [[url: 'https://github.com/princemitnick/ci-cd-testing.git']]
        ])
      }
    }

    stage('Compute Version Tags') {
      steps {
        script {
          def version = sh(script: "git describe --tags --abbrev=0", returnStdout: true).trim()
          def commit = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
          def buildNumber = env.BUILD_NUMBER

          IMAGE_NAME = "${DOCKERHUB_USERNAME}/${IMAGE_REPO}"
          TAG_VERSION = "${IMAGE_NAME}:${version}"
          TAG_COMMIT = "${IMAGE_NAME}:${commit}-${buildNumber}"
          TAG_LATEST = "${IMAGE_NAME}:latest"

          echo "🔖 Tags générés :"
          echo "  - ${TAG_VERSION}"
          echo "  - ${TAG_COMMIT}"
          echo "  - ${TAG_LATEST}"
        }
      }
    }

    stage('Build & Tag Docker Image') {
      steps {
        script {
          sh """
            docker build --build-arg CACHEBUST=$(date +%s) -t ${TAG_VERSION} .
            docker tag ${TAG_VERSION} ${TAG_COMMIT}
            docker tag ${TAG_VERSION} ${TAG_LATEST}
          """
        }
      }
    }

    stage('Security Scan - Trivy') {
      steps {
        script {
          echo "🔐 Scan Trivy (bloquant si vulnérabilités CRITICAL)"
          sh """
            trivy image --severity CRITICAL ${TAG_VERSION}
          """
        }
      }
    }

    stage('Smoke Test') {
      steps {
        script {
          sh "docker run -d --name fastapi_test -p 8000:8000 ${TAG_VERSION}"
          sleep time: 5, unit: 'SECONDS'
          def status = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/health", returnStdout: true).trim()

          sh "docker stop fastapi_test || true"
          sh "docker rm fastapi_test || true"

          if (status != '200') {
            error("L’image ne répond pas. Code HTTP : ${status}")
          } else {
            echo "L’image répond avec HTTP ${status}"
          }
        }
      }
    }

    stage('Push to DockerHub') {
      when {
        expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
      }
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS_ID}", usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
          script {
            sh "echo $PASSWORD | docker login -u $USER --password-stdin ${DOCKER_REGISTRY}"
            sh "docker push ${TAG_VERSION}"
            sh "docker push ${TAG_COMMIT}"
            sh "docker push ${TAG_LATEST}"
          }
        }
      }
    }

    stage('Export Build Info') {
      steps {
        script {
          def metadata = """
            {
              "version": "${TAG_VERSION}",
              "commit": "${TAG_COMMIT}",
              "latest": "${TAG_LATEST}",
              "build_number": "${env.BUILD_NUMBER}",
              "git_commit": "$(git rev-parse HEAD)"
            }
          """
          writeFile file: 'buildInfo.json', text: metadata
          archiveArtifacts artifacts: 'buildInfo.json', fingerprint: true
        }
      }
    }

    stage('Cleanup') {
      steps {
        script {
          sh "docker rmi ${TAG_VERSION} ${TAG_COMMIT} ${TAG_LATEST} || true"
        }
      }
    }
  }

  post {
    success {
      echo "Déploiement réussi. Tous les tests et scans sont OK."
    }
    failure {
      echo "Échec du pipeline. Merci de vérifier les logs."
    }
    always {
      cleanWs()
      echo "Workspace nettoyé."
    }
  }
}