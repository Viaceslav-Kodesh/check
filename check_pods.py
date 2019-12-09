from kubernetes import client, config
import time
import sys
from kubernetes.client import CoreV1Api
import os
# Configs can be set in Configuration class directly or using helper utility


if os.path.isfile('./config'):
    print ("Kubeconfig exist")
else:
    print ("Kubeconfig not exist")
    os.system('openstack coe cluster delete $OS_CLUSTER_NAME')
    sys.exit(1)

array = []

try:
   config.load_kube_config()
except:
    print("Could not load kube config")
    os.system('openstack coe cluster delete $OS_CLUSTER_NAME')
    sys.exit(1)

v1 = client.CoreV1Api()
try:
   ret = v1.list_pod_for_all_namespaces(watch=False)
except:
    print("Could not connect to cluster or something wrong with config")
    os.system('openstack coe cluster delete $OS_CLUSTER_NAME')
    sys.exit(1)

for i in ret.items:
   if i.status.phase != "Running":
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
        os.system('kubectl get po --all-namespaces')
        os.system('openstack coe cluster delete $OS_CLUSTER_NAME')
        sys.exit(0)
    else:
        time.sleep(10)
        count += 1

if len(array) != 0 and count == 10:
    for i in array:
        print("%s\t%s\t%s" % (i.metadata.name, i.metadata.namespace, i.status.phase))
        os.system('openstack coe cluster delete $OS_CLUSTER_NAME')
        sys.exit(1)
