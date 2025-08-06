pipeline {
  agent any

  stages {
    stage('Hello') {
      steps {
        echo "Creating docker images and running container"
      }
    }

    stage('Clone Repository') {
      steps {
        git branch: 'main', url: 'https://github.com/utsav0514/Book_store.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          docker build -t djimage:v1 .
          docker tag djimage:v1 utsav0514/djimage:v1
        '''
      }
    }

    stage('Run Docker Container') {
      steps {
        sh '''
          docker stop book_bar || true 
          docker rm -f book_bar || true 
          docker run -d --name book_bar -p 8000:8000 utsav0514/djimage:v1
        '''
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'Docker-hub-id', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push utsav0514/djimage:v1
            docker logout
          '''
        }
      }
    }
  }
}
