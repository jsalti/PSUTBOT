def compareAndSaveHash(dataList, hashFile) {
    echo "Debug: dataList = ${dataList}"
    def currentHashes = []

    for (def data in dataList) {
        // Use a consistent encoding, such as UTF-8
        def currentHash = sh(script: """echo -n "${data}" | ${PYTHON_EXECUTABLE} -c "import hashlib; import sys; print(hashlib.md5(sys.stdin.buffer.read()).hexdigest())" """, returnStdout: true).trim()
        currentHashes.add(currentHash)
    }

    def previousHash = ""
    if (fileExists(hashFile)) {
        previousHash = readFile(hashFile).trim()
    }

    if (currentHashes.join('\n') == previousHash) {
        echo "Data has not changed. Skipping further processing."
        return false
    } else {
        writeFile file: hashFile, text: currentHashes.join('\n')
        echo "Data has changed. Continuing with further processing."
        return true
    }
}



def handleError(e, stageName) {
    echo "Error in stage '${stageName}': ${e.message}"
    def stackTrace = e.toString()
    echo "Stack trace:"
    echo stackTrace
    currentBuild.result = 'FAILURE'
}

pipeline {
    agent any

    environment {
        CLUB_DATA_HASH_FILE = 'club_data_hash.txt'
        STUDENT_LIFE_DATA_HASH_FILE = 'student_life_data_hash.txt'
        SCHOOL_DATA_HASH_FILE = 'school_data_hash.txt'
        MASTER_PROGRAMS_DATA_HASH_FILE = 'master_programs_data_hash.txt'
        FAQ_DATA_HASH_FILE = 'faq_data_hash.txt'
        STAFF_DATA_HASH_FILE = 'staff_data_hash.txt'
        ACADEMIC_CALENDAR_HASH_FILE = 'academic_calendar_data_hash.txt'
        BUS_SCHEDULE_HASH_FILE = 'bus_schedule_hash.txt'
        OFFICE_HOURS_HASH_FILE = 'office_hours_hash.txt'
        STUDY_PLANS_HASH_FILE = 'study_plans_hash.txt'
        OUTPUT_DIRECTORY = '/tmp'
        changesBoolean = true
        PYTHON_EXECUTABLE = '/Users/jinnyy/anaconda3/bin/python'
        PATH = "/usr/local/bin:${env.PATH}:${PYTHON_EXECUTABLE}"
        DB_NAME = 'PSUTBOT'
        REPO_URL = 'https://github.com/jsalti/PSUTBOT.git'
        REPO_BRANCH = 'main'
        SCRIPTS_DIRECTORY = 'scripts'
        CHANGES_CHECK_INTERVAL = 5
    }
    stages {
        stage('Create Directories') {
            steps {
                script {
                    sh """
                        mkdir -p ${OUTPUT_DIRECTORY}/output_event \
                                   ${OUTPUT_DIRECTORY}/output_staff \
                                   ${OUTPUT_DIRECTORY}/output_school \
                                   ${OUTPUT_DIRECTORY}/output_masters \
                                   ${OUTPUT_DIRECTORY}/output_faq \
                                   ${OUTPUT_DIRECTORY}/output_club \
                                   ${OUTPUT_DIRECTORY}/output_academic_calendar
                    """
                }
            }
        }

        stage('Checkout Code') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/jsalti/PSUTBOT.git']]])
            }
        }

        stage('Scrape & Insert Academic Calendar Data') {
            steps {
                script {
                    if (changesBoolean) {
                        echo 'Executing Python script for scraping academic calendar data...'
                        try {
                            def academicCalendarScriptPath = "${SCRIPTS_DIRECTORY}/scrape_and_insert_academic_calendar_data.py"
                            def scrapedData = sh(script: "${PYTHON_EXECUTABLE} ${academicCalendarScriptPath} --scrape-academic-calendar", returnStdout: true).trim()
                            compareAndSaveHash([scrapedData], ACADEMIC_CALENDAR_HASH_FILE)
                            sh(script: "${PYTHON_EXECUTABLE} ${academicCalendarScriptPath} --insert-into-mongodb", returnStatus: true)
                        } catch (Exception e) {
                            handleError(e, 'Scrape Academic Calendar Data')
                        }
                    } else {
                        error('Terminating stage - no need to scrape')
                    }
                }
            }
        }
        stage('Scrape & Insert Club Information') {
            steps {
                script {
                    if (changesBoolean) {
                        echo 'Executing Python script for scraping club information...'
                        try {
                            def clubScriptPath = "${SCRIPTS_DIRECTORY}/scrape_and_insert_club_information.py"
                            def scrapedData = sh(script: "${PYTHON_EXECUTABLE} ${clubScriptPath} --scrape-club-data", returnStdout: true).trim()
                            echo "Environment Variables: ${env}"
                            compareAndSaveHash([scrapedData], CLUB_DATA_HASH_FILE)
                            sh(script: "${PYTHON_EXECUTABLE} ${clubScriptPath} --insert-into-mongodb", returnStatus: true)
                            
                        } catch (Exception e) {
                            handleError(e, 'Scrape Club Information')
                            
                        }
                        
                    } else {
                        error('Terminating stage - no need to scrape')
                        
                    }
                    
                }
                
            }
            
        }

        stage('Scrape & Insert FAQ Information') {
            steps {
                script {
                    if (changesBoolean) {
                        echo 'Executing Python script for scraping FAQ information...'
                        try {
                            def faqScriptPath = "${SCRIPTS_DIRECTORY}/scrape_and_insert_faq_info.py"
                            def scrapedData = sh(script: "${PYTHON_EXECUTABLE} ${faqScriptPath} --scrape-faq", returnStdout: true).trim()
                            echo "Environment Variables: ${env}"
                            compareAndSaveHash([scrapedData], FAQ_DATA_HASH_FILE)
                            sh(script: "${PYTHON_EXECUTABLE} ${faqScriptPath} --scrape-faq", returnStatus: true)

                            
                        } catch (Exception e) {
                            handleError(e, 'Scrape FAQ Information')
                            
                        }
                        
                    } else {
                        error('Terminating stage - no need to scrape')
                        
                    }
                    
                }
                
            }
            
        }
        stage('Scrape & Insert School Information') {
            steps {
                script {
                    if (changesBoolean) {
                        echo 'Executing Python script for scraping school information...'
                        try {
                            def schoolScriptPath = "${SCRIPTS_DIRECTORY}/scrape_and_insert_school_info.py"
                            def scrapedData = sh(script: "${PYTHON_EXECUTABLE} ${schoolScriptPath} --scrape-and-insert", returnStdout: true).trim()
                            echo "Environment Variables: ${env}"
                            compareAndSaveHash([scrapedData], SCHOOL_DATA_HASH_FILE)
                            sh(script: "${PYTHON_EXECUTABLE} ${schoolScriptPath} --scrape-and-insert", returnStatus: true)
                            
                        } catch (Exception e) {
                            handleError(e, 'Scrape School Information')
                            
                        }
                        
                    } else {
                        error('Terminating stage - no need to scrape')
                        
                    }
                    
                }
                
            }
            
        }
        stage('Scrape & Insert Staff Information') {
            steps {
                script {
                    if (changesBoolean) {
                        echo 'Executing Python script for scraping staff information...'
                        try {
                            def staffScriptPath = "${SCRIPTS_DIRECTORY}/scrape_and_insert_staff_info.py"
                            def scrapedData = sh(script: "${PYTHON_EXECUTABLE} ${staffScriptPath} --scrape-and-insert", returnStdout: true).trim()
                            echo "Environment Variables: ${env}"
                            compareAndSaveHash([scrapedData], STAFF_DATA_HASH_FILE)
                            sh(script: "${PYTHON_EXECUTABLE} ${staffScriptPath} --scrape-and-insert", returnStatus: true)
                            
                        } catch (Exception e) {
                            handleError(e, 'Scrape Staff Information')
                            
                        }
                        
                    } else {
                        error('Terminating stage - no need to scrape')
                        
                    }
                    
                }
                
            }
            
        }
        stage('Scrape & Insert Student Life Activities') {
            steps {
                script {
                    if (changesBoolean) {
                        echo 'Executing Python script for scraping student life activities...'
                        try {
                            def studentLifeScriptPath = "${SCRIPTS_DIRECTORY}/scrape_and_insert_student_life_activities.py"
                            def scrapedData = sh(script: "${PYTHON_EXECUTABLE} ${studentLifeScriptPath} --scrape-and-insert", returnStdout: true).trim()
                            echo "Environment Variables: ${env}"
                            compareAndSaveHash([scrapedData], STUDENT_LIFE_DATA_HASH_FILE)
                            sh(script: "${PYTHON_EXECUTABLE} ${studentLifeScriptPath} --scrape-and-insert", returnStatus: true)
                            
                        } catch (Exception e) {
                            handleError(e, 'Scrape Student Life Activities')
                            
                        }
                        
                    } else {
                        error('Terminating stage - no need to scrape')
                        
                    }
                    
                }
                
            }
            
        }
        stage('Scrape & Insert Master Programs Information') {
            steps {
                script {
                    if (changesBoolean) {
                        echo 'Executing Python script for scraping master programs information...'
                        try {
                            def masterProgramsScriptPath = "${SCRIPTS_DIRECTORY}/scrape_and_insert_master_programs_info.py"
                            def scrapedData = sh(script: "${PYTHON_EXECUTABLE} ${masterProgramsScriptPath} --scrape-master-programs", returnStdout: true).trim()
                            echo "Environment Variables: ${env}"
                            compareAndSaveHash([scrapedData."master_Program_Name"], MASTER_PROGRAMS_DATA_HASH_FILE)
                            compareAndSaveHash([scrapedData."master_Program_Description"], MASTER_PROGRAMS_DATA_HASH_FILE)
                            sh(script: "${PYTHON_EXECUTABLE} ${masterProgramsScriptPath} --insert-into-mongodb", returnStatus: true)
                            
                        } catch (Exception e) {
                            handleError(e, 'Scrape & Insert Master Programs Information')
                            
                        }
                        
                    } else {
                        error('Terminating stage - no need to scrape')
                        
                    }
                    
                }
                
            }
            
        }
        stage('Insert Bus Schedule') {
            steps {
                script {
                    echo 'Inserting Bus Schedule data into MongoDB...'
                    try {
                        def busScheduleScriptPath = "${SCRIPTS_DIRECTORY}/insert_busschedule.py"
                        sh(script: "${PYTHON_EXECUTABLE} ${busScheduleScriptPath}", returnStatus: true)
                        
                    } catch (Exception e) {
                        handleError(e, 'Insert Bus Schedule')
                        
                    }
                    
                }
                
            }
            
        }
        stage('Insert Office Hours') {
            steps {
                script {
                    echo 'Inserting Office Hours data into MongoDB...'
                    try {
                        def officeHoursScriptPath = "${SCRIPTS_DIRECTORY}/insert_office_hrs.py"
                        sh(script: "${PYTHON_EXECUTABLE} ${officeHoursScriptPath}", returnStatus: true)
                    } catch (Exception e) {
                        handleError(e, 'Insert Office Hours')
                    }
                }
            }
        }
        stage('Insert Study Plans Links') {
            steps {
                script {
                    echo 'Inserting Study Plans Links data into MongoDB...'
                    try {
                        def studyPlansScriptPath = "${SCRIPTS_DIRECTORY}/insert_studyplans.py"
                        sh(script: "${PYTHON_EXECUTABLE} ${studyPlansScriptPath}", returnStatus: true)
                        
                    } catch (Exception e) {
                        handleError(e, 'Insert Study Plans Links')
                        
                    }
                    
                }
                
            }
            
        }
    }
}
