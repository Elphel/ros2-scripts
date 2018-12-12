#!/usr/bin/env python3

import asyncio
import xml.etree.ElementTree as ET
import rclpy
from elphel_interfaces.srv import StrReqStrRes
import ros2_config

TIMEOUT = 5


# master callbacks
def signup_callback(req,res):

  name = req.request

  print('Sign up from '+name)

  if name in clients:
    print('Slave name is not unique. So sad.')
  else:
    clients.append(name)

  print('List of registered slaves: '+str(clients))
  res.response = name

  return res


# async coroutine for cmdall_callback
async def pass_cmd(target,cmd):

  node = rclpy.create_node(target+'_client')
  cli = node.create_client(StrReqStrRes,target+'/cmd')

  wcnt = 0
  while not cli.wait_for_service(timeout_sec=1.0):
    print('Service is not available, waiting '+str(wcnt)+'...')
    wcnt += 1
    if wcnt==TIMEOUT:
      break

  req = StrReqStrRes.Request()
  req.request = cmd

  cli.call(req)
  cli.wait_for_future()

  cmdres = cli.response.response
  return cmdres


# callback for broadcast commands
def cmdall_callback(req,res):

  cmd = req.request
  tasks = [pass_cmd(c,cmd) for c in clients]
  results = event_loop.run_until_complete(asyncio.gather(*tasks))

  print(results)

  res.response = '\n'.join(results)

  return res


# global
clients = []
cfg = ros2_config.get()

nodename = cfg[0]['name']

for i in cfg:
  clients.append(i['name'])

rclpy.init()
node = rclpy.create_node(nodename+"_master")

event_loop = asyncio.get_event_loop()

print("Starting master services:")
#print("  master/signup")
#s1 = node.create_service(StrReqStrRes, 'master/signup',  signup_callback)
print("  master/cmd_all")
s2 = node.create_service(StrReqStrRes, 'master/cmd_all', cmdall_callback)

rclpy.spin(node)

# Destroy the node explicitly
# (optional - Done automatically when node is garbage collected)
node.destroy_node()
rclpy.shutdown()

event_loop.close()
