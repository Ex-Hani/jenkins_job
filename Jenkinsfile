pipeline {
    agent any
    parameters {
        file(name: 'EXCEL_FILE', description: 'Excel file to process')
        booleanParam(name: 'RUN_CREATE_QUESTIONARY_FIELDS', defaultValue: false, description: 'Run create_questionary_fields.py')
        booleanParam(name: 'RUN_CREATE_VACANCY_FIELDS', defaultValue: false, description: 'Run create_vacancy_fields.py')
    }
    environment {
        PYTHON = '/usr/bin/python3'
        REPO_URL = 'git@github.com:Ex-Hani/jenkins_job.git'
        SCRIPTS_DIR = 'scripts/schema/vacancy_request_creator'
    }
    stages {
        stage('Clone repository') {
            steps {
                script {
                    def GITHUB_TOKEN = credentials('github-token') ?: ''
                    // Клонировать репозиторий
                    sh "git clone ${REPO_URL}"
                }
            }
        }
        stage('Install dependencies') {
            steps {
                script {
                    // Перейти в каталог с скриптами
                    dir(SCRIPTS_DIR) {
                        // Установить зависимости
                        sh '''
                            ${PYTHON} -m pip install requests~=2.26.0
                            ${PYTHON} -m pip install urllib3~=1.26.6
                            ${PYTHON} -m pip install Brotli==1.0.9
                            ${PYTHON} -m pip install certifi==2021.10.8
                            ${PYTHON} -m pip install charset-normalizer==2.0.12
                            ${PYTHON} -m pip install idna==3.3
                            ${PYTHON} -m pip install multivolumefile==0.2.3
                            ${PYTHON} -m pip install psutil==5.9.1
                            ${PYTHON} -m pip install py7zr==0.18.9
                            ${PYTHON} -m pip install pybcj==0.6.0
                            ${PYTHON} -m pip install pycryptodomex==3.15.0
                            ${PYTHON} -m pip install pyppmd==0.18.2
                            ${PYTHON} -m pip install pyzstd==0.15.2
                            ${PYTHON} -m pip install telebot==0.0.4
                            ${PYTHON} -m pip install texttable==1.6.4
                            ${PYTHON} -m pip install zipfile-deflate64==0.2.0
                            ${PYTHON} -m pip install openpyxl==2.6.4
                            ${PYTHON} -m pip install loguru==0.7.0
                            ${PYTHON} -m pip install python-dotenv==0.21.0
                            ${PYTHON} -m pip install pyperclip==1.8.2
                        '''
                    }
                }
            }
        }
        stage('Run main script') {
            steps {
                script {
                    // Проверить, что файл загружен и напечатать его имя
                    if (fileExists(params.EXCEL_FILE)) {
                        echo "Excel file path: ${params.EXCEL_FILE}"
                        // Запустить основной скрипт с параметрами
                        sh "${PYTHON} ${SCRIPTS_DIR}/main.py --input_file ${params.EXCEL_FILE}"
                    } else {
                        error "Файл ${params.EXCEL_FILE} не найден"
                    }
                }
            }
        }
        stage('Optional scripts') {
            steps {
                script {
                    // Опционально запустить create_questionary_fields.py
                    if (params.RUN_CREATE_QUESTIONARY_FIELDS) {
                        sh "${PYTHON} ${SCRIPTS_DIR}/create_questionary_fields.py"
                    }
                    // Опционально запустить create_vacancy_fields.py
                    if (params.RUN_CREATE_VACANCY_FIELDS) {
                        sh "${PYTHON} ${SCRIPTS_DIR}/create_vacancy_fields.py"
                    }
                }
            }
        }
        stage('Archive output') {
            steps {
                script {
                    // Архивировать выходной файл для загрузки
                    archiveArtifacts artifacts: '**/output_file.*', allowEmptyArchive: true
                }
            }
        }
        stage('Version') {
            steps {
                sh 'python3 --version'
            }
        }
        stage('Hello') {
            steps {
                sh 'python3 main.py'
            }
        }
    }
}
