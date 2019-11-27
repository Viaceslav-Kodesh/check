from kubernetes import client, config
import time
import sys
from kubernetes.client import CoreV1Api
import os
# Configs can be set in Configuration class directly or using helper utility

config.load_kube_config()
v1 = client.CoreV1Api()
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
   if i.status.phase != "Running":
       array = []
       array.append(i)

count = 0
while(count < 10):

    for i in array:
       core_v1 = CoreV1Api()
       resp = None
       resp = core_v1.read_namespaced_pod(name=i.metadata.name,namespace='kube-system')
       print(resp.metadata.name)
       if resp.status.phase == "Running":
           array.remove(i)

    if len(array) == 0:
        count=10
        os.system('openstack coe cluster delete vks-test')
        sys.exit(0)
    else:
        time.sleep(1)
        count += 1

if len(array) != 0 and count == 10:
    for i in array:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.status.phase))
        os.system('openstack coe cluster delete vks-test')
        sys.exit(1)
