import http.client
import urllib.parse
import json
import time


def getUserStatus(user):
    conn = http.client.HTTPConnection("www.codeforces.com");
    url = urllib.parse.quote("http://codeforces.com/api/user.status?handle=%s&from=1&count=1000" % user, safe=':/?=&');
    conn.request("GET", url);
    res = conn.getresponse();
    ans = res.read().decode("utf-8");
    tt = json.loads(ans);
    ff = 'user_status/%s.json' % user;
    if tt['status'] != 'OK':
        return False;
    print('OK  ' + url);
    with open(ff,'w') as f:
        json.dump(tt, f);
    return True



with open('user_list.json','r') as f:
    users = json.load(f);

for handle in users:
    print(getUserStatus(handle));
    time.sleep(0.2);
