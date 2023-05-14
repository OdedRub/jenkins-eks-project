pipeline {
    agent none
    
    stages {
        stage('Clone repository') {
            agent { label "blue" }
            steps {
                git branch: 'main', credentialsId: 'github-finegrained', url: 'https://github.com/OdedRub/project_1/'
            }
        }
        stage('Build') { 
            agent { label "blue" }
            steps { 
                sh '''
                GIT_COMMIT=$(git rev-parse HEAD)
                docker build -t 718666525897.dkr.ecr.eu-central-1.amazonaws.com/project_1:$GIT_COMMIT ./weather_app
                '''
            }
        }
        stage('Push Artifact') {
            agent { label "blue" }
            steps {
                script{
                        docker.withRegistry('https://718666525897.dkr.ecr.eu-central-1.amazonaws.com/project_1', 'ecr:eu-central-1:aws-credents') {
                            sh '''
                            GIT_COMMIT=$(git rev-parse HEAD)
                            docker push 718666525897.dkr.ecr.eu-central-1.amazonaws.com/project_1:$GIT_COMMIT
                            '''
                    }
                }
            }
        }
        stage('Deploy'){
            agent { label "blue" }
            steps {
                script {
                    withKubeConfig([credentialsId: 'K8S', serverUrl: '']) {
	                catchError (buildResult: 'SUCCESS', message: 'No such resources') {
	                sh 'kubectl delete cm image-config replica-config' 
	                }
                    sh '''
                    GIT_COMMIT=$(git rev-parse HEAD)
                    kubectl apply -f ./kubernetes/image-config.yml -f ./kubernetes/replica-config.yml
                    kubectl describe cm replica-config
                    kubectl apply -f ./kubernetes/Service.yml -f ./kubernetes/Deployment.yml
                    kubectl apply -f ./kubernetes/Nginx-ingress-1.yml
                    kubectl apply -f ./kubernetes/Ingress.yaml
                    kubectl get service -o wide
                    kubectl describe cm image-config
                    '''
                  }
                }
            }   
        }
    }
}
// test
