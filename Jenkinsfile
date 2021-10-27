def getVariables(branch) {
    if (branch == 'origin/develop') {
        return ['3.68.97.65', 'top-fastapi-dev']
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
         configFileProvider(
            [configFile(fileId: env.config_file, targetLocation: 'config')]) {
                 sh 'sudo docker build --tag fast_api_demo .'
                 sh 'sudo docker run -d --name fast_api_demo fast_api_demo:latest'
            }
       }
     }
     stage('Save image') {
       steps {
         sh 'sudo docker save fast_api_demo > fast_api_demo.tar'
       }
     }

     stage('Deploy') {
       steps {
         script {
          def baseDir = '/projects/garments_api'
          def loadImage = 'sudo docker load < fast_api_demo.tar'
          def docker_compose_restart = 'sudo docker-compose up -d'

           sshagent(credentials : ['ssh_credentials']) {
             sh "scp fast_api_demo jenkins@${env.server_ip}:${baseDir}"
             sh "ssh jenkins@${env.server_ip} 'cd ${baseDir} && ${loadImage} && ${docker_compose_restart}'"
           }
         }
       }
     }
   }
   post {
     always {
       sh 'sudo docker stop fast_api_demo && sudo docker rm fast_api_demo'
       sh 'sudo rm fast_api_demo.tar'
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
