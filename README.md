# ros2-scripts

* Mostly python3 scripts for Elphel 393 multi-camera systems to init and work. 
* Can be run on PC as well.
* Do not need to be built as a ROS2 package. See instructions below for running on PC.
* The basic idea is there's a single master and multiple slaves. Master is responsible for:
  * init, sequential or parallel - depending on the system configuration, e.g. a slave can be power up dependent on another slave. 
  * broadcast commands, e.g. some daemons on/off
* Example list of services (cam_* are slaves),:
```
~$ ros2 service list
/cam_101698/cmd
/cam_1467cd/cmd
/master/cmd_all
```
* Master creates 2 nodes, e.g.:
```
~$ ros2 node list
cam_1467cd
cam_101698
cam_101698_master
```



## Instructions
### Camera
* To be included into *init_elphel393.py* for autorun
* To launch manually:
```sh
~$ ssh root@camera-ip
~# cd /etc/elphel393
~# python3 ros2_init.py
```
* To enable **master** node, edit the */etc/elphel393/ros2_config.xml*:
```
<ros2>
  <prefix>cam_</prefix>
  <role>master</role>
  <node name='cam_101698' role='left'/>
  <node name='cam_1467cd' role='pc'/>
</ros2>
```
<node>-tag is for slave cameras, where *name* attr is a prefix and the last 3 octets of the slave's MAC (eth0). *role* must not be '**master**', not yet very meaningful.

### PC
```sh
~$ source /opt/ros/<distro>/setup.sh
~$ source ~/ros2_ws/install/setup.sh # must have ros2-interfaces installed
~$ cd repo-path 
# make changes to ros2_config.xml
~$ python3 ros2_init.py
```

## ros2_config.py
* Loads the deafult config xml (*ros2_config.xml*) and reads MAC (from /sys/class/net/(eth|wlp|enp))/address) - based on the MAC and prefix from config the slave node is named.

## Command line example for sending request to a service
```
~$ ros2 service call /master/cmd_all elphel_interfaces/StrReqStrRes "{'request':'ls -all'}"
```
