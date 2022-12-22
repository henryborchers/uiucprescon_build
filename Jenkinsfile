pipeline {
    agent none
    options {
        timeout(time: 1, unit: 'DAYS')
    }
    stages{
        stage('Testing'){
            agent {
                dockerfile {
                    filename 'ci/docker/linux/jenkins/Dockerfile'
                    label 'linux && docker'
                    additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                }
            }
            stages{
                stage('Setting up'){
                    steps{
                        sh 'mkdir -p reports'
                    }
                }
                stage('Run Checks'){
                    parallel{
                        stage('Pylint'){
                            steps{
                                withEnv(['PYLINTHOME=/tmp/.cache/pylint']) {
                                    catchError(buildResult: 'SUCCESS', message: 'Pylint found issues', stageResult: 'UNSTABLE') {
                                        sh(label: 'Running pylint',
                                            script: 'pylint uiucprescon.build -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint.txt'
                                        )
                                    }
                                }
                            }
                            post{
                                always{
                                    recordIssues(tools: [pyLint(pattern: 'reports/pylint.txt')])
                                    stash includes: 'reports/pylint_issues.txt,reports/pylint.txt', name: 'PYLINT_REPORT'
                                }
                            }
                        }
                        stage('Flake8') {
                            steps{
                                catchError(buildResult: 'SUCCESS', message: 'flake8 found some warnings', stageResult: 'UNSTABLE') {
                                    sh(label: 'Running flake8',
                                       script: 'flake8 uiucprescon --tee --output-file=logs/flake8.log'
                                    )
                                }
                            }
                            post {
                                always {
                                    stash includes: 'logs/flake8.log', name: 'FLAKE8_REPORT'
                                    recordIssues(tools: [flake8(name: 'Flake8', pattern: 'logs/flake8.log')])
                                }
                            }
                        }
                        stage('MyPy') {
                            steps{
                                catchError(buildResult: 'SUCCESS', message: 'MyPy found issues', stageResult: 'UNSTABLE') {
                                    sh(
                                        label: 'Running Mypy',
                                        script: '''mkdir -p logs
                                                   mypy -p uiucprescon --html-report reports/mypy/html > logs/mypy.log
                                                   '''
                                   )
                                }
                            }
                            post {
                                always {
                                    recordIssues(tools: [myPy(name: 'MyPy', pattern: 'logs/mypy.log')])
                                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy/html/', reportFiles: 'index.html', reportName: 'MyPy HTML Report', reportTitles: ''])
                                }
                            }
                        }
                    }
                }
            }
            post{
                cleanup{
                    cleanWs(
                        deleteDirs: true,
                        patterns: [
                            [pattern: 'reports/', type: 'INCLUDE'],
                            [pattern: 'logs/', type: 'INCLUDE'],
                        ]
                    )
                }
            }
        }
    }
}
