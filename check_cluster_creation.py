import os
import json
import time
import sys

count = 0
while(count < 10):
        os.system('openstack coe cluster list --format json >result.json')
        filename = 'result.json'
        with open('result.json') as json_file:
            data = json.load(json_file)
            for p in data:
                print(p['status'])
            if p['status'] == "CREATE_COMPLETE":
                                              count=10
                                              sys.exit(0)
            if p['status'] == "CREATE_FAILED":
                                              count=10
            else:
                time.sleep(60)
                count += 1


if p['status'] == "CREATE_FAILED" and count == 10:
                                                 sys.exit(1)