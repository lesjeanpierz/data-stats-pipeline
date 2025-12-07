pipeline {

    options {
        skipDefaultCheckout(true)
    }

    agent {
        kubernetes {
            label 'python-agent'
            yaml """
apiVersion: v1
kind: Pod
spec:
  workspaceVolume:
    emptyDirWorkspaceVolume: {}
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
                    dir("${WORKSPACE}") {
                        sh '''
                            pip install pandas openpyxl matplotlib requests
                            python src/fetch_insee_data.py
                        '''
                    }
                }
            }
        }

        stage('Commit & Push generated files') {
            steps {
                container('python') {
                    dir("${WORKSPACE}") {

                        withCredentials([string(credentialsId: 'github-pat', variable: 'GITHUB_TOKEN')]) {

                            sh '''
                                echo "Git directory:"
                                ls -la .git

                                git config user.name "jenkins-bot"
                                git config user.email "jenkins-bot@example.com"

                                git remote set-url origin https://${GITHUB_TOKEN}@github.com/lesjeanpierz/data-stats-pipeline.git

                                git add revenu_disponible_brut.png revenu_disponible_brut.xlsx || true
                                git commit -m "Mise à jour automatique" || echo "Rien à commit"
                                git push origin main
                            '''
                        }
                    }
                }
            }
        }
    }
}
