#!/usr/bin/env python3

import subprocess
import ros2_config

cfg = ros2_config.get()

if   cfg[0]['role']=='master':
  subprocess.Popen(['python3','ros2_master.py'])

subprocess.Popen(['python3','ros2_slave.py'])
