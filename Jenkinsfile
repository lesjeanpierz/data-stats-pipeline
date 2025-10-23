pipeline {
    agent {
        kubernetes {
            label 'python-agent'
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: python
    image: python:3.12
    command:
    - cat
    tty: true
"""
        }
    }

    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/lesjeanpierz/data-stats-pipeline.git',
                    credentialsId: 'github-pat'
            }
        }

        stage('Run Python script') {
            steps {
                container('python') {
                    sh '''
                    pip install pandas openpyxl matplotlib requests
                    python src/fetch_insee_data.py
                    '''
                }
            }
        }
    }
}

