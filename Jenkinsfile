pipeline {
    agent any

    environment {
        CLUB_DATA_HASH_FILE = 'club_data_hash.txt'
        STUDENT_LIFE_DATA_HASH_FILE = 'student_life_data_hash.txt'
        SCHOOL_DATA_HASH_FILE = 'school_data_hash.txt'
        MASTER_PROGRAMS_DATA_HASH_FILE = 'master_programs_data_hash.txt'
        FAQ_DATA_HASH_FILE = 'faq_data_hash.txt'
        STAFF_DATA_HASH_FILE = 'staff_data_hash.txt'
        ACADEMIC_CALENDAR_DATA_HASH_FILE = 'academic_calendar_data_hash.txt'
        OUTPUT_DIRECTORY = '/tmp'
        changesBoolean = true // added a global boolean variable
    }

    stages {
        stage('Create Directories') {
            steps {
                script {
                    sh "mkdir -p ${OUTPUT_DIRECTORY}/output_event ${OUTPUT_DIRECTORY}/output_staff ${OUTPUT_DIRECTORY}/output_school ${OUTPUT_DIRECTORY}/output_masters ${OUTPUT_DIRECTORY}/output_faq ${OUTPUT_DIRECTORY}/output_club ${OUTPUT_DIRECTORY}/output_academic_calendar"
                }
            }
        }

        stage('Checkout Code') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/jsalti/PSUTBOT.git']]])
            }
        }

        stage('Scrape Club Information') {
            steps {
                script {
                    if (changesBoolean) {
                        echo 'Executing Python script for scraping club information...'
                        try {
                            sh 'python scripts/scrape_club_information.py'
                            sleep time: 5, unit: 'SECONDS' // Delay to ensure file is written
                            compareAndSaveHash("${OUTPUT_DIRECTORY}/output_club/club_information.json", CLUB_DATA_HASH_FILE)
                        } catch (Exception e) {
                            handleError(e, 'Scrape Club Information')
                        }
                    } else {
                        error('Terminating stage - no need to scrape')
                    }
                }
            }
        }

        // Add similar stages for other information
        stage('Scrape Student Life Activities') {
            steps {
                script {
                    echo 'Executing Python script for scraping student life activities...'
                    try {
                        sh 'python scripts/scrape_student_life_activities.py'
                        sleep time: 5, unit: 'SECONDS'
                        compareAndSaveHash("${OUTPUT_DIRECTORY}/output_event/student_life_activities.json", STUDENT_LIFE_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e, 'Scrape Student Life Activities')
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
                        sleep time: 5, unit: 'SECONDS'
                        compareAndSaveHash("${OUTPUT_DIRECTORY}/output_school/all_combined_data.json", SCHOOL_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e, 'Scrape School Information')
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
                        sleep time: 5, unit: 'SECONDS'
                        compareAndSaveHash("${OUTPUT_DIRECTORY}/output_masters/master_programs_data.json", MASTER_PROGRAMS_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e, 'Scrape Master Programs Information')
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
                        sleep time: 5, unit: 'SECONDS'
                        compareAndSaveHash("${OUTPUT_DIRECTORY}/output_faq/faq_data.json", FAQ_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e, 'Scrape FAQ Information')
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
                        sleep time: 5, unit: 'SECONDS'
                        compareAndSaveHash("${OUTPUT_DIRECTORY}/output_staff/staff_info.json", STAFF_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e, 'Scrape Staff Information')
                    }
                }
            }
        }

        stage('Extract Academic Calendar Data') {
            steps {
                script {
                    echo 'Executing Python script for extracting academic calendar data...'
                    try {
                        // Ensure ChromeDriver is available for extract_academic_calendar_data.py
                        sh 'python scripts/extract_academic_calendar_data.py'
                        sleep time: 5, unit: 'SECONDS'
                        compareAndSaveHash("${OUTPUT_DIRECTORY}/output_academic_calendar/extracted_data.json", ACADEMIC_CALENDAR_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e, 'Extract Academic Calendar Data')
                    }
                }
            }
        }
        
        stage('Insert Club Information into MongoDB') {
            steps {
                script {
                    echo 'Inserting club information into MongoDB...'
                    try {
                        sh 'python database/insert_club_information_to_mongodb.py'
                    } catch (Exception e) {
                        handleError(e, 'Insert Club Information into MongoDB')
            }
        }
    }
}
        stage('Insert Student Life Activities into MongoDB') {
            steps {
                script {
                    echo 'Inserting student life activities into MongoDB...'
                    try {
                        sh 'python database/insert_student_life_activities_to_mongodb.py'
                    } catch (Exception e) {
                        handleError(e, 'Insert Student Life Activities into MongoDB')
            }
        }
    }
}

        stage('Final Stage') {
            steps {
                echo 'Pipeline finished successfully.'
            }
        }
    }
}

def compareAndSaveHash(dataFile, hashFile) {
    def currentHash = ""
    if (isUnix()) {
        currentHash = sh(script: "md5 -q \"${dataFile}\"", returnStdout: true).trim()
    } else if (isWindows()) {
        currentHash = sh(script: "certutil -hashfile \"${dataFile}\" MD5 | findstr /i /v \"md5\"", returnStdout: true).trim()
    }

    def previousHash = ""
    if (fileExists(hashFile)) {
        previousHash = readFile(hashFile).trim()
    }

    if (currentHash == previousHash) {
        echo "Data has not changed. Skipping further processing."
        changesBoolean = false // updated changesBoolean to false
        currentBuild.result = 'SUCCESS'
    } else {
        writeFile file: hashFile, text: currentHash
        echo "Data has changed. Continuing with further processing."
    }
}

def handleError(e, stageName) {
    echo "Error in stage '${stageName}': ${e.message}"
    currentBuild.result = 'FAILURE'
    // Consider adding more detailed error logging here
}
