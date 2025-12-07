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

        stage('Commit & Push generated files') {
            steps {
                container('python') {

                    withCredentials([string(credentialsId: 'github-pat', variable: 'GITHUB_TOKEN')]) {

                        sh '''
                            echo "📌 Configuration de Git dans le conteneur"

                            git config user.name "jenkins-bot"
                            git config user.email "jenkins-bot@example.com"

                            # On change l'URL du remote pour injecter le token
                            git remote set-url origin https://${GITHUB_TOKEN}@github.com/lesjeanpierz/data-stats-pipeline.git

                            echo "📌 Ajout des fichiers générés"
                            git add revenu_disponible_brut.png revenu_disponible_brut.xlsx || true

                            echo "📌 Commit si nécessaire"
                            git commit -m "Mise à jour automatique des fichiers INSEE" || echo "Rien à commit"

                            echo "📌 Push vers GitHub"
                            git push origin main
                        '''
                    }
                }
            }
        }
    }
}
