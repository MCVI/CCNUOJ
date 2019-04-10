from flask import g

from .util import http, get_request_json
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import Contest, User, Problem
from .authentication import require_authentication

import math
import json
import numpy as np
from sklearn.externals import joblib

PredictPath = "predict_related_data/"

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

# 求用户的特征值
def calcUserEigenvalue(handle):
    with open(PredictPath + 'problemdict.json','r') as f:
        p_dict = json.load(f)         # 读入题库字典
    with open(PredictPath + 'user_status/%s.json' % handle) as f:
        user_status = json.load(f)    # 读入用户提交数据
    status_dict = dict(); # 通过记rating，不通过记-1
    for submission in user_status['result']:
        problem = submission['problem']
        if problem.get('contestId') == None:
            continue
        ret = findProblem(problem['contestId'], problem['name'], p_dict);
        if ret == None:
            continue
        key = ret['num']
        if status_dict.get(key) == None:
            status_dict[key] = -1
        if submission['verdict'] == 'OK':
            status_dict[key] = ret['rating']
    with open(PredictPath + 'user_result/%s.json' % handle, 'w') as f:
        json.dump(status_dict, f)
    
    cluster = np.load(PredictPath + 'Kmeans15.npy'); # 读入聚类结果
    K = cluster.max() + 1
    sqr_value = np.zeros(K)
    number = np.zeros(K)
    for res in status_dict:
        if status_dict[res]==-1:
            continue
        cluster_k = cluster[res]
        rating = status_dict[res]
        sqr_value[cluster_k] += rating * rating
        number[cluster_k] += 1
    engin_value = np.zeros(K)
    for i in range(K):
        if number[i] == 0:
            continue
        engin_value[i] = math.sqrt(sqr_value[i]/number[i])
    np.save(PredictPath + 'user_engin_value/%s' % handle, engin_value)
    return engin_value

def predict(handles, problemNum, cluster_K = 15):
    module = joblib.load(PredictPath + 'problem_module/%d.pickle' % problemNum)
    N = len(handles)
    X = np.zeros([N,cluster_K])
    for i in range(N):
        handle = handles[i]
        engin_value = calcUserEigenvalue(handle)
        X[i] = engin_value
    proba = module.predict_proba(X)
    return proba

# 'pass' 'undo' 'try but unpassed'
def getResult(handle, problemId):
    with open(PredictPath + 'user_result/%s.json' % handle, 'r') as f:
        user_result = json.load(f)
    problemId = str(problemId)
    if user_result.get(problemId) == None:
        return 'undo'
    if user_result[problemId] > 0:
        return 'pass'
    return 'try but unpassed'


# 选出最高highest_k个能解除第problemId道题的用户
def highest_proba_users(problemId, highest_k, handles):
    proba = predict(handles, problemId)
    ret = list()
    problem = Problem.query.get(problemId)
    title = ""
    if problem != None:
        title = getattr(problem, "title")
    for i in range(len(handles)):
        tmp = {'problemId':problemId, 'title':title, 'handle':handles[i], 'probability' : proba[i][1]}
        ret.append(tmp);
    ret.sort(key=lambda x: x['probability'], reverse=True)
    ans = list()
    n = min(highest_k, len(ret))
    for i in range(n):
        ans.append(ret[i])
        ans[i]['result'] = getResult(ans[i]['handle'], problemId)
    return ans

@bp.route("/help/predict/<int:id>", methods=["GET"])
def retrieve_help_predict(id):
    fileName = 'user_list.json'
    with open(PredictPath + fileName,'r') as f:
        handles = json.load(f)
    instance = {
        "result": highest_proba_users(id, 10, handles),
    }
    return http.Success(result=instance)


def recommend_problem(handle, num, maxID=50):
    handles = [handle]
    ret = list()
    for i in range(maxID):
        tmp = highest_proba_users(i+1, 1, handles)
        res = getResult(handle, tmp[0]['problemId'])
        if res == 'pass':
            continue
        proba = tmp[0]['probability']
        if proba < 0.3:
            continue
        if proba > 0.7:
            continue
        tmp[0]['result'] = res
        ret.append(tmp[0])
    ret.sort(key=lambda x: x['probability'], reverse=True)
    ans = list()
    n = min(num, len(ret))
    for i in range(n):
        ans.append(ret[i])
    return ans


@bp.route("/help/recommend/<string:handle>", methods=["GET"])
def retrieve_recommend_problem(handle):
    instance = {
        "result": recommend_problem(handle, 5),
    }
    return http.Success(result=instance)