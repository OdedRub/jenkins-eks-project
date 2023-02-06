pipeline {
    agent none
    
    stages {
        stage('Clone repository') {
            agent { label "blue" }
            steps { 
                //git branch: 'main', url: 'https://github.com/OdedRub/project_1.git'
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
                    //sh '''
                    //curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                    //unzip awscliv2.zip
                    //sudo ./aws/install
                    //'''
                    //sh '''
                    //curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.21.2/2021-07-05/bin/linux/amd64/kubectl
                    //chmod +x ./kubectl
                    //mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
                    //echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc
                    //'''
                    sh '''
                    kubectl apply -f ./kubernetes/Service.yml -f ./kubernetes/Deployment.yml -f ./kubernetes/Configmap.yml
                    def elb_dns = sh(returnStdout: true, script: 'aws elb describe-load-balancers --load-balancer-names weather-service --query "LoadBalancerDescriptions[0].DNSName"').trim()
                    echo "ELB DNS: ${elb_dns}"
                    sh "./deploy.sh ${elb_dns}"
                    kubectl apply -f ./kubernetes/Nginx-ingress-1.yml
                    kubectl apply -f ./kubernetes/Ingress.yaml
                    '''
                  }
                }
            }   
        }
    }
}
