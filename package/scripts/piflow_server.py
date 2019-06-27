import os
import base64
from time import sleep
from resource_management import *

class PiFlowServerMaster(Script):
    
    def install(self, env):
        Directory('/data/piflow/',
              mode=0755,
              cd_access='a',
              create_parents=True
        )
        Execute('cd /data/piflow/')
        Execute('cd /data/piflow/ && wget https://github.com/cas-bigdatalab/piflow/releases/download/v0.5/piflow.tar.gz')
        Execute('cd /data/piflow/ && tar -xvf piflow.tar.gz && mv piflow piflowServer')
        Execute('cd /data/piflow/ && rm -rf  piflow.tar.gz')
        Execute('sudo -u hdfs hdfs dfs -mkdir -p /apps/piflow/checkpoints/')
        Execute('sudo -u hdfs hdfs dfs -mkdir -p /apps/piflow/debug/')
       

    def configure(self, env):  
        import params
        env.set_params(params)
        piflow_sever = InlineTemplate(params.piflow_sever)   
        File(format("/data/piflow/piflowServer/config.properties"), content=piflow_sever)

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('cd /data/piflow/piflowServer/ && nohup sh start.sh > nohup.out 2>&1 &', ignore_failures=True)
        Execute("ps -ef | grep java | grep piflow-server-0.9.jar | grep -v grep | awk '{print $2}' >/data/piflow/piflowServer/ps.pid")
      
    def stop(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('cd /data/piflow/piflowServer/ && sh stop.sh', ignore_failures=True)


    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/data/piflow/piflowServer/ps.pid")


if __name__ == "__main__":
    PiFlowServerMaster().execute()
