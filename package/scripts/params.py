from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob,socket

# server configurations
config = Script.get_config()
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
piflow_sever=config['configurations']['piflow']['piflow_sever']
piflow_web=config['configurations']['piflow']['piflow_web']
current_host_name = socket.gethostname()
