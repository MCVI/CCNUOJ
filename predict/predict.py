import numpy as np
import json
from sklearn.externals import joblib

def predict(handles, problemNum, cluster_K = 15):
    module = joblib.load('problem_module/%d.pickle' % problemNum);
    N = len(handles);
    X = np.zeros([N,cluster_K]);
    for i in range(N):
        handle = handles[i];
        engin_value = np.load('user_engin_value/%s.npy' % handle);
        X[i] = engin_value;
    proba = module.predict_proba(X);
    return proba;

# for test
ans = predict(["Out_of_Cage", "Out_of_Cage"],1);
print(ans);
