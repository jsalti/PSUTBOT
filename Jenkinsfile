pipeline {
    agent any

    environment {
        // Define variables to store the hash of the extracted data for each stage
        CLUB_DATA_HASH_FILE = 'club_data_hash.txt'
        STUDENT_LIFE_DATA_HASH_FILE = 'student_life_data_hash.txt'
        SCHOOL_DATA_HASH_FILE = 'school_data_hash.txt'
        MASTER_PROGRAMS_DATA_HASH_FILE = 'master_programs_data_hash.txt'
        FAQ_DATA_HASH_FILE = 'faq_data_hash.txt'
        STAFF_DATA_HASH_FILE = 'staff_data_hash.txt'
        ACADEMIC_CALENDAR_DATA_HASH_FILE = 'academic_calendar_data_hash.txt'
    }

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
                    echo 'Executing Python script for scraping club information...'
                    try {
                        sh 'python scripts/scrape_club_information.py'
                        compareAndSaveHash('club_information.json', env.CLUB_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e)
                    }
                }
            }
        }

        stage('Scrape Student Life Activities') {
            steps {
                script {
                    echo 'Executing Python script for scraping student life activities...'
                    try {
                        sh 'python scripts/scrape_student_life_activities.py'
                        compareAndSaveHash('student_life_activities.json', env.STUDENT_LIFE_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e)
                    }
                }
            }
        }

        stage('Scrape School Information') {
            steps {
                script {
                    echo 'Executing Python script for scraping school information...'
                    try {
                        sh 'python scripts/scrape_school_info.py'
                        compareAndSaveHash('all_combined_data.json', env.SCHOOL_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e)
                    }
                }
            }
        }

        stage('Scrape Master Programs Information') {
            steps {
                script {
                    echo 'Executing Python script for scraping master programs information...'
                    try {
                        sh 'python scripts/scrape_master_programs_info.py'
                        compareAndSaveHash('master_programs_data.json', env.MASTER_PROGRAMS_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e)
                    }
                }
            }
        }

        stage('Scrape FAQ Information') {
            steps {
                script {
                    echo 'Executing Python script for scraping FAQ information...'
                    try {
                        sh 'python scripts/scrape_faq_info.py'
                        compareAndSaveHash('faq_data.json', env.FAQ_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e)
                    }
                }
            }
        }

        stage('Scrape Staff Information') {
            steps {
                script {
                    echo 'Executing Python script for scraping staff information...'
                    try {
                        sh 'python scripts/scrape_staff_info.py'
                        compareAndSaveHash('staff_info.json', env.STAFF_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e)
                    }
                }
            }
        }

        stage('Extract Academic Calendar Data') {
            steps {
                script {
                    echo 'Executing Python script for extracting academic calendar data...'
                    try {
                        sh 'python scripts/extract_academic_calendar_data.py'
                        compareAndSaveHash('extracted_data.json', env.ACADEMIC_CALENDAR_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e)
                    }
                }
            }
        }

        // Add more stages as needed
    }

    post {
        always {
            // You can add cleanup or finalization steps here if needed
        }
    }

    // Function to compare hashes and save the current hash to the file
    def compareAndSaveHash(dataFile, hashFile) {
        def currentHash = sh(script: "md5sum ${dataFile} | awk '{print $1}'", returnStdout: true).trim()
        def previousHash = readFile(hashFile).trim()

        if (currentHash == previousHash) {
            echo "Data has not changed. Skipping further processing."
            currentBuild.result = 'SUCCESS'
            return
        }

        writeFile file: hashFile, text: currentHash
    }

    // Function to handle errors and set the build result to FAILURE
    def handleError(Exception e) {
        echo "Error: ${e.message}"
        currentBuild.result = 'FAILURE'
    }
}
