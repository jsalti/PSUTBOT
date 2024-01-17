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
        PYTHON_EXECUTABLE = '/Users/jinnyy/anaconda3/bin/python'
        PATH = "${PYTHON_EXECUTABLE}:${env.PATH}"
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
                            sh "${PYTHON_EXECUTABLE} scripts/scrape_club_information.py"
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

        stage('Scrape Student Life Activities') {
            steps {
                script {
                    echo 'Executing Python script for scraping student life activities...'
                    try {
                        sh "${PYTHON_EXECUTABLE} scripts/scrape_student_life_activities.py"
                        sleep time: 5, unit: 'SECONDS'
                        compareAndSaveHash("${OUTPUT_DIRECTORY}/output_event/student_life_activities.json", STUDENT_LIFE_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e, 'Scrape Student Life Activities')
                    }
                }
            }
        }



        stage('Scrape Master Programs Information') {
            steps {
                script {
                    echo 'Executing Python script for scraping master programs information...'
                    try {
                        sh "${PYTHON_EXECUTABLE} scripts/scrape_master_programs_info.py"
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
                        sh "${PYTHON_EXECUTABLE} scripts/scrape_faq_info.py"
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
                        sh "${PYTHON_EXECUTABLE} scripts/scrape_staff_info.py"
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
                        sh "${PYTHON_EXECUTABLE} scripts/extract_academic_calendar_data.py"
                        sleep time: 5, unit: 'SECONDS'
                        compareAndSaveHash("${OUTPUT_DIRECTORY}/output_academic_calendar/extracted_data.json", ACADEMIC_CALENDAR_DATA_HASH_FILE)
                    } catch (Exception e) {
                        handleError(e, 'Extract Academic Calendar Data')
                    }
                }
            }
        }

        stage('Insert Data into MongoDB') {
            steps {
                script {
                    parallel(
                        'Club Information': {
                            echo 'Inserting club information into MongoDB...'
                            try {
                                sh "${PYTHON_EXECUTABLE} database/insert_club_information_to_mongodb.py"
                            } catch (Exception e) {
                                handleError(e, 'Insert Club Information into MongoDB')
                            }
                        },
                        'Student Life Activities': {
                            echo 'Inserting student life activities into MongoDB...'
                            try {
                                sh "${PYTHON_EXECUTABLE} database/insert_student_life_activities_to_mongodb.py"
                            } catch (Exception e) {
                                handleError(e, 'Insert Student Life Activities into MongoDB')
                            }
                        },
                        'School Information': {
                            echo 'Inserting school information into MongoDB...'
                            try {
                                sh "${PYTHON_EXECUTABLE} database/insert_school_info_to_mongodb.py"
                            } catch (Exception e) {
                                handleError(e, 'Insert School Information into MongoDB')
                            }
                        },
                        'Master Programs Information': {
                            echo 'Inserting master programs information into MongoDB...'
                            try {
                                sh "${PYTHON_EXECUTABLE} database/insert_master_programs_to_mongodb.py"
                            } catch (Exception e) {
                                handleError(e, 'Insert Master Programs Information into MongoDB')
                            }
                        },
                        'FAQ Information': {
                            echo 'Inserting FAQ information into MongoDB...'
                            try {
                                sh "${PYTHON_EXECUTABLE} database/insert_faq_to_mongodb.py"
                            } catch (Exception e) {
                                handleError(e, 'Insert FAQ Information into MongoDB')
                            }
                        },
                        'Staff Information': {
                            echo 'Inserting staff information into MongoDB...'
                            try {
                                sh "${PYTHON_EXECUTABLE} database/insert_staff_Info_to_mongodb.py"
                            } catch (Exception e) {
                                handleError(e, 'Insert Staff Information into MongoDB')
                            }
                        },
                        'Academic Calendar Data': {
                            echo 'Inserting academic calendar data into MongoDB...'
                            try {
                                sh "${PYTHON_EXECUTABLE} database/insert_academic_calender_to_mongodb.py"
                            } catch (Exception e) {
                                handleError(e, 'Insert Academic Calendar Data into MongoDB')
                            }
                        },
                        'Study Plans': {
                            echo 'Inserting study plans into MongoDB...'
                            try {
                                sh "${PYTHON_EXECUTABLE} database/insert_StudyPlans_to_mongodb.py"
                            } catch (Exception e) {
                                handleError(e, 'Insert Study Plans into MongoDB')
                            }
                        },
                        'Bus Schedule': {
                            echo 'Inserting bus schedule into MongoDB...'
                            try {
                                sh "${PYTHON_EXECUTABLE} database/insert_busschedule_to_mongodb.py"
                            } catch (Exception e) {
                                handleError(e, 'Insert Bus Schedule into MongoDB')
                            }
                        },
                        'Office Hours': {
                            echo 'Inserting office hours into MongoDB...'
                            try {
                                sh "${PYTHON_EXECUTABLE} database/insert_office_hours_to_mongodb.py"
                            } catch (Exception e) {
                                handleError(e, 'Insert Office Hours into MongoDB')
                            }
                        }
                    )
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
        currentHash = sh(script: "${PYTHON_EXECUTABLE} -c \"import hashlib; print(hashlib.md5(open('${dataFile}', 'rb').read()).hexdigest())\"", returnStdout: true).trim()
    } else if (isWindows()) {
        currentHash = bat(script: "${PYTHON_EXECUTABLE} -c \"import hashlib; print(hashlib.md5(open('${dataFile}', 'rb').read()).hexdigest())\"", returnStdout: true).trim()
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
