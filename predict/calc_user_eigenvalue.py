import numpy as np
import json
import math

np.set_printoptions(formatter={'float': '{: 0.4f}'.format});

# 求problem的num, rating等
def findProblem(contestId, name, p_dict):
    for i in [-1,0,1]:
        c = str(contestId + i);
        if p_dict.get(c) == None:
            continue;
        problems = p_dict[c];
        for p in problems:
            if p['name'] == name:
                return p;
    return None;

def calcUserEigenvalue(handle):
    with open('problemdict.json','r') as f:
        p_dict = json.load(f);         # 读入题库字典
    with open('user_status/%s.json' % handle) as f:
        user_status = json.load(f);    # 读入用户提交数据
    status_dict = dict(); # 通过记rating，不通过记-1
    for submission in user_status['result']:
        problem = submission['problem'];
        if problem.get('contestId') == None:
            continue;
        ret = findProblem(problem['contestId'], problem['name'], p_dict);
        if ret == None:
            continue;
        key = ret['num'];
        if status_dict.get(key) == None:
            status_dict[key] = -1;
        if submission['verdict'] == 'OK':
            status_dict[key] = ret['rating'];
    with open('user_result/%s.json' % handle, 'w') as f:
        json.dump(status_dict, f);
    
    cluster = np.load('Kmeans15.npy'); # 读入聚类结果
    K = cluster.max() + 1;
    sqr_value = np.zeros(K);
    number = np.zeros(K);
    for res in status_dict:
        if status_dict[res]==-1:
            continue;
        cluster_k = cluster[res];
        rating = status_dict[res];
        sqr_value[cluster_k] += rating * rating;
        number[cluster_k] += 1;
    engin_value = np.zeros(K);
    for i in range(K):
        if number[i] == 0:
            continue;
        engin_value[i] = math.sqrt(sqr_value[i]/number[i]);
    np.save('user_engin_value/%s' % handle, engin_value);
    return engin_value;

# for test
ans = calcUserEigenvalue("Out_of_Cage");
print(ans);
