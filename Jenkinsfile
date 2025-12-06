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

        stage('Commit & Push results') {
            steps {
                sh """
                    git config user.email "jenkins-bot@yourdomain.com"
                    git config user.name "Jenkins Bot"

                    git add revenu_disponible_brut.png revenu_disponible_brut.xlsx

                    git commit -m "Mise à jour automatique des fichiers générés par Jenkins" || echo "Rien à commit"

                    git push origin HEAD:${BRANCH_NAME}
                """
            }
        }
    }
}

    }
}

