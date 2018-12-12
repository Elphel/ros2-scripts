#!/usr/bin/env python3

import os
import re
import xml.etree.ElementTree as ET

def is_unique_name(a,name):
  for i in a:
    if i['name']==name:
      return False
  return True

# get function
def get(f="ros2_config.xml"):

  cfg = []

  prefix = "cam_"
  mac = get_mac(capitalize=False)
  name = prefix+mac

  role = "unknown"

  if os.path.isfile(f):
    e = ET.parse(f).getroot()

    tmp = e.find('prefix')
    if tmp!=None:
      name = tmp.text+mac

    tmp = e.find('role')
    if tmp!=None:
      role = tmp.text

    # self goes first
    cfg.append({'name':name,
                'role':role})

    # drop non-unique names
    for s in e.findall('node'):

      tmp_name = s.get('name')
      tmp_role = s.get('role')

      if is_unique_name(cfg,tmp_name):
        cfg.append({'name': tmp_name,
                    'role': tmp_role})
      # will not overwrite role for non-unique nodes

  return cfg


# get mac function
def get_mac(last_three_octets=True, keep_colons=False, capitalize=True):

  mac = "00:00:00:00:00:00"

  for root, dirs, files in os.walk("/sys/class/net/"):
    for name in dirs:
      # enp or wlp will work for linux pc for testing
      if re.match('(eth|enp|wlp)',name):
        fname = os.path.join(root,name,'address')
        #print(fname)
        with open(fname, 'r') as content_file:
          mac = content_file.read().strip()
        break

  if last_three_octets:
    mac = mac[-8:]

  if not keep_colons:
    mac = re.sub(':','',mac)

  if capitalize:
    mac = mac.upper()

  return mac




# MAIN
if __name__ == "__main__":

  # Test 1
  mac = get_mac()
  print(mac)

  # Test 2
  mac = get_mac(last_three_octets=False,keep_colons=True,capitalize=False)
  print(mac)