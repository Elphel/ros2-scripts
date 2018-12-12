#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import rclpy

from elphel_interfaces.srv import StrReqStrRes
import ros2_config

rclpy.init()
node = rclpy.create_node('some_client_node')

cli = node.create_client(StrReqStrRes, 'master/cmd_all')

wcnt = 0
while not cli.wait_for_service(timeout_sec=1.0):
  print('Service is not available, waiting '+str(wcnt)+'...')
  wcnt += 1

req = StrReqStrRes.Request()
req.request = "wget -qO- -o /dev/null 'http://localhost/parsedit.php?immediate&TRIG'"

cli.call(req)
cli.wait_for_future()

res = cli.response.response

node.get_logger().info("cmd response:")
node.get_logger().info(res)

node.destroy_node()
rclpy.shutdown()