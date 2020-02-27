import os
import json
import time
import sys
import requests
# test1111

def telegram_bot_sendtext(bot_message):

    bot_token = os.environ['OS_TELEGRAM_TOKEN']
    bot_chatID = os.environ['OS_TELEGRAM_CHAT_ID']
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

telegram_bot_sendtext("Process of k8s creation has been started")

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
    telegram_bot_sendtext(str(err))
    os.system('openstack coe cluster delete $OS_CLUSTER_NAME')
    sys.exit(1)
