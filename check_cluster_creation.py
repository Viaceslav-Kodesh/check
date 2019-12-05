import os
import json
import time
import sys

count = 0
while(count < 10):
        os.system('openstack coe cluster show $OS_CLUSTER_NAME -c status --format json >result.json')
        filename = 'result.json'
        with open('result.json') as json_file:
            data = json.load(json_file)

            if data['status'] == "CREATE_COMPLETE":
                count=10
                sys.exit(0)
            if data['status'] == "CREATE_FAILED":
                count=10
            else:
                time.sleep(60)
                count += 1


if data['status'] == "CREATE_FAILED" and count == 10:
    os.system('openstack coe cluster show $OS_CLUSTER_NAME -c status_reason -c faults --format json >err.json')
    filename = 'err.json'
    with open('err.json') as json_file:
        err = json.load(json_file)
    print err
    os.system('openstack coe cluster delete $OS_CLUSTER_NAME')
    sys.exit(1)
