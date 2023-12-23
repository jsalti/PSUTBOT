pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                // Clone the GitHub repository
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/jsalti/PSUTBOT.git']]])
            }
        }

        stage('Scrape Club Information') {
            steps {
                script {
                    sh 'scripts/scrape_club_information.py'
                }
            }
        }

        stage('Scrape Student Life Activities') {
            steps {
                script {
                    sh 'scripts/scrape_student_life_activities.py'
                }
            }
        }

        stage('Scrape School Information') {
            steps {
                script {
                    sh 'scripts/scrape_school_info.py'
                }
            }
        }

        stage('Scrape Master Programs Information') {
            steps {
                script {
                    sh 'scripts/scrape_master_programs_info.py'
                }
            }
        }

        stage('Scrape FAQ Information') {
            steps {
                script {
                    sh 'scripts/scrape_faq_info.py'
                }
            }
        }

        stage('Scrape Staff Information') {
            steps {
                script {
                    sh 'scripts/scrape_staff_info.py'
                }
            }
        }

        stage('Extract Academic Calendar Data') {
            steps {
                script {
                    sh 'scripts/extract_academic_calendar_data.py'
                }
            }
        }

        stage('Check for Data Changes') {
            steps {
                script {
                    // Implement logic to check if data has changed
                    def previousDataPath = 'path/to/previous_data.json'
                    def currentDataPath = 'path/to/current_data.json'

                    if (fileExists(previousDataPath) && fileCompare(previousDataPath, currentDataPath)) {
                        currentBuild.result = 'ABORTED'
                        echo 'No changes detected. Aborting the build.'
                    }
                }
            }
        }

        stage('Create Vectorized Database') {
            steps {
                script {
                    // Implement logic to create a vectorized database
                    // This could be a separate script or set of commands
                }
            }
        }

        stage('Train Chatbot Model') {
            steps {
                script {
                    // Implement logic to train your chatbot model
                    // This could be a separate script or set of commands
                }
            }
        }
    }
}

def fileExists(filePath) {
    return fileExistsOrNot(filePath) == "EXISTS"
}

def fileCompare(file1, file2) {
    return file1.text == file2.text
}

def fileExistsOrNot(filePath) {
    def file = new File(filePath)
    if (file.exists()) {
        return "EXISTS"
    } else {
        return "NOT EXISTS"
    }
}
