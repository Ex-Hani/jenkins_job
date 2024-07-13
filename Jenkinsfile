pipeline {
    agent any

    parameters {
        string(name: 'EXCEL_FILE_PATH', defaultValue: '', description: 'Path to the Excel file to process')
    }

    environment {
        // Укажите здесь, где находятся ваши скрипты, например, путь к Python виртуальному окружению
        PYTHON_ENV = '/path/to/python/env'
        SCRIPT_PATH = 'https://github.com/Ex-Hani/jenkins_job/blob/main/main.py'
        SCRIPT_NAME = 'main.py'
    }

    stages {
        stage('Checkout') {
            steps {
                // Клонируем репозиторий
                git branch: 'main', url: 'https://github.com/Ex-Hani/jenkins_job.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Устанавливаем зависимости, если требуется
                    sh "${env.PYTHON_ENV}/bin/pip install -r requirements.txt"
                }
            }
        }

        stage('Run Script') {
            steps {
                script {
                    // Запускаем Python скрипт с параметрами
                    sh """
                    ${env.PYTHON_ENV}/bin/python ${env.SCRIPT_NAME} \\
                    --input_file ${params.EXCEL_FILE_PATH} \\
                    --folder_name output \\
                    --output_path ./output
                    """
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'output/**', allowEmptyArchive: true
        }
        cleanup {
            cleanWs()
        }
    }
}
