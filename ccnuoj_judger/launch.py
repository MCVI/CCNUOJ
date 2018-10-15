from time import sleep

import requests


api_base = "http://localhost:5000"

with open("local_config.txt", "rt") as config:
    token = config.read().strip('\n')

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
                    print("Execution has not yet implemented")
        sleep(1)

    except requests.RequestException as e:
        print("Error occurred:")
        print(e)
