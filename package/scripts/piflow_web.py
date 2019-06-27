import os
import base64
from time import sleep
from resource_management import *

class PiFlowWebMasterMaster(Script):
    
    def install(self, env):
        Execute('cd /data/piflow/ && wget https://github.com/cas-bigdatalab/piflow-web/releases/download/0.5/piflow-web.tar.gz')
        Execute('cd /data/piflow/ && tar -xvf piflow-web.tar.gz && mv piflow-web piflowWeb')
        Execute('cd /data/piflow/ && rm -rf  piflow-web.tar.gz')
        Execute('mkdir -p /data/piflow/piflowWeb/storage/image')
        Execute('mkdir -p /data/piflow/piflowWeb/storage/piflow')
        Execute('mkdir -p /data/piflow/piflowWeb/storage/xml')
        Execute('mkdir -p /data/piflow/piflowWeb/storage/video')

    def configure(self, env):  
        import params
        env.set_params(params)
        piflow_web = InlineTemplate(params.piflow_web)   
        File(format("/data/piflow/piflowWeb/config.properties"), content=piflow_web)


    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('cd /data/piflow/piflowWeb/ && sh start.sh', ignore_failures=True)
        Execute("ps -ef | grep java | grep piflow-web.jar | grep -v grep | awk '{print $2}' >/data/piflow/piflowWeb/pw.pid")

    def stop(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('cd /data/piflow/piflowWeb/ && sh stop.sh', ignore_failures=True)


    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/data/piflow/piflowWeb/pw.pid")


if __name__ == "__main__":
    PiFlowWebMasterMaster().execute()
