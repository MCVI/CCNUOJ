from time import sleep

import requests

from command import execute
from local_config import api_base, token


session = requests.Session()
session.headers.update({"X-CCNU-AUTH-TOKEN": token})

while True:
    try:
        instance = session.get(api_base+"/judge_command/unfetched/5").json()
        if instance["status"] != "Success":
            print("Failed")
            print("Reason: %s" % instance["reason"])
        else:
            result = instance["result"]
            for obj in result:
                fetch_response = session.post(api_base+"/judge_command/%d/fetched" % obj["id"]).json()
                if fetch_response["status"] != "Success":
                    print("Failed to fetch judge command #%d" % obj["id"])
                    print("Reason: %s" % fetch_response["reason"])
                else:
                    print("Successfully fetched judge command #%d: %s" % (obj["id"], obj["command"]))
                    execute(obj["command"])

    except requests.RequestException as e:
        print("Error occurred:")
        print(e)

    sleep(1)
