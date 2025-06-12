pipeline {
  agent any

  environment {
    IMAGE_NAME = "myapi-fastapi"
    CONTAINER_NAME = "myapi-container"
    TARGET_URL = "http://localhost:8000"
    REPORT_HTML = "zap_report.html"
  }

  stages {

    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/princemitnick/ci-cd-testing.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh "docker build -t ${IMAGE_NAME} ."
      }
    }

    stage('Run Container') {
      steps {
        sh '''
          docker run -d --rm --name ${CONTAINER_NAME} -p 8000:8000 ${IMAGE_NAME}
          sleep 10
        '''
      }
    }

    stage('Run OWASP ZAP Scan') {
      steps {
        sh '''
          docker run --rm -v $(pwd):/zap/wrk/:rw \
            ghcr.io/zaproxy/zaproxy zap-baseline.py \
            -t ${TARGET_URL}/health \
            -r ${REPORT_HTML}
        '''
      }
    }

    stage('Archive Report') {
      steps {
        archiveArtifacts artifacts: "${REPORT_HTML}", onlyIfSuccessful: true
      }
    }
  }

  post {
    always {
      sh "docker stop ${CONTAINER_NAME} || true"
    }
  }
}