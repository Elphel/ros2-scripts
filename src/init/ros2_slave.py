#!/usr/bin/env python3

import subprocess
import xml.etree.ElementTree as ET

import rclpy
from elphel_interfaces.srv import StrReqStrRes
import ros2_config

TIMEOUT = 5

# slave callbacks
def cmd_callback(req,res):
  cmd = req.request
  # call to localhost here, get response and send it back
  try:
    output = subprocess.check_output(cmd,shell=True)
  except subprocess.CalledProcessError:
    output = "<error>-1</error>"

  res.response = '<cmd><node>'+nodename+'</node><status>'+str(output)+'</status></cmd>'

  return res

# global
cfg = ros2_config.get()

nodename = cfg[0]['name']

rclpy.init()
node = rclpy.create_node(nodename)

# now start cmd service
print("Starting slave services:")
print("  "+nodename+'/cmd')
s3 = node.create_service(StrReqStrRes, nodename+'/cmd', cmd_callback)

rclpy.spin(node)

# Destroy the node explicitly
# (optional - Done automatically when node is garbage collected)
node.destroy_node()
rclpy.shutdown()