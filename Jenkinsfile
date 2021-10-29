def getVariables(branch) {
    if (branch == 'origin/develop') {
        return ['3.70.193.141', 'top-fastapi-dev']
    } else {
        error("Unkown branch checked out")
    }
}

pipeline {
   agent { label 'linux' }
   environment {
     vars = getVariables(env.GIT_BRANCH)
     server_ip = vars.get(0)
     config_file = vars.get(1)
   }
   options { gitLabConnection('Default') }
   stages {
     stage('Build') {
       steps {
         configFileProvider(docker
            [configFile(fileId: env.config_file, targetLocation: 'src/config/')]) {
                 sh 'sudo docker build --tag fast_api_demo .'
                 sh 'sudo docker tag fast_api_demo:latest pttrnsdevelopers/top-fast-api:latest'
            }
       }
     }
     stage('Push image') {
       steps {
         sh 'sudo docker push pttrnsdevelopers/top-fast-api:tagname'
       }
     }
     stage('Deploy') {
       steps {
         script {
          def baseDir = '/projects/garments_api'
          def loadImage = 'sudo docker pull pttrnsdevelopers/top-fast-api:latest'
          def docker_compose_restart = 'sudo docker-compose up -d'

           sshagent(credentials : ['ssh_credentials']) {
             sh "ssh jenkins@${env.server_ip} 'cd ${baseDir} && ${loadImage} && ${docker_compose_restart}'"
           }
         }
       }
     }
   }
   post {
     always {
       script {
         String status
         switch (currentBuild.currentResult) {
           case 'SUCCESS':
             status = 'success'
             break
           default:
              emailext body: '$DEFAULT_CONTENT', postsendScript: '$DEFAULT_POSTSEND_SCRIPT', presendScript: '$DEFAULT_PRESEND_SCRIPT', recipientProviders: [developers()], replyTo: '$DEFAULT_REPLYTO', subject: '$DEFAULT_SUBJECT', to: '$DEFAULT_RECIPIENTS'
              status = 'failed'
              break
         }
         updateGitlabCommitStatus(name: 'build', state: status)
       }
     }
   }
 }
