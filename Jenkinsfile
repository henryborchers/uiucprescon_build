pipeline {
    agent none
    options {
        timeout(time: 1, unit: 'DAYS')
    }
    stages{
        stage('Building and Testing'){
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
                stage('Building Docs'){
                    steps{
                        sh 'python -m sphinx -W --keep-going -b html docs build/docs -w logs/build_sphinx_html.log'
                    }
                    post{
                        always{
                            recordIssues(tools: [sphinxBuild(pattern: 'logs/build_sphinx_html.log')])
                        }
                        cleanup{
                            cleanWs(
                                notFailBuild: true,
                                deleteDirs: true,
                                patterns: [
                                    [pattern: 'build/', type: 'INCLUDE'],
                                ]
                            )
                        }
                    }
                }
                stage('Run Checks'){
                    parallel{
                        stage('PyTest'){
                            steps{
                                catchError(buildResult: 'UNSTABLE', message: 'Did not pass all pytest tests', stageResult: 'UNSTABLE') {
                                    sh(
                                        label: 'Running Pytest',
                                        script:'''mkdir -p reports/coverage
                                                  coverage run --parallel-mode --source=uiucprescon -m pytest --junitxml=reports/pytest.xml
                                                  '''
                                   )
                               }
                            }
                            post {
                                always {
                                    junit 'reports/pytest.xml'
                                }
                            }
                        }
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
                    post{
                        always{
                            sh(label: 'combining coverage data',
                               script: '''coverage combine
                                          coverage xml -o ./reports/coverage-python.xml
                                          sed -i 's/uiucprescon\\/build\\///' reports/coverage-python.xml
                                          '''
                            )
                            archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/coverage-python.xml'
                            publishCoverage(
                                adapters: [
                                        coberturaAdapter(mergeToOneReport: true, path: 'reports/coverage*.xml')
                                    ],
                                sourceFileResolver: sourceFiles('STORE_ALL_BUILD'),
                           )
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
