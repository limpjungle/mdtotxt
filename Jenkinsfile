pipeline {
    agent any

    environment {
        // Name and tag of image
        IMAGE_NAME = 'convert:latest'

    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Need plugin Docker Pipeline
                    docker.build("${IMAGE_NAME}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "### Тестовый заголовок" > test_input.md
                    echo "Это **жирный** текст." >> test_input.md

                    # Запускаем контейнер, монтируя рабочую папку
                    docker run --rm -v "$(pwd):/data" ${IMAGE_NAME}:${BUILD_NUMBER} test_input.md -o test_output.txt

                    if [ ! -f test_output.txt ]; then
                        echo "Ошибка: test_output.txt не создан"
                        exit 1
                    fi

                    # Проверяем, что в полученном тексте есть фразы без разметки
                    if grep -q "Тестовый заголовок" test_output.txt && grep -q "Это жирный текст." test_output.txt; then
                        echo "Тест пройден"
                    else
                        echo "Тест не пройден: содержимое не соответствует ожидаемому"
                        cat test_output.txt
                        exit 1
                    fi
                '''
            }
        }

        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Log in and push image to Registry
                    docker.withRegistry("https://${REGISTRY}", "${DOCKER_CREDENTIALS}") {
                        def appImage = docker.image("${IMAGE_NAME}:${BUILD_NUMBER}")
                        appImage.push()                // version with number of build
                        appImage.push('latest')        // latest tag
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
