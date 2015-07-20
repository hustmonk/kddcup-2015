#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

import math
from sklearn import linear_model, decomposition, datasets
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation
from sklearn import metrics
import sklearn
import logging
import logging.config
import sys
import cPickle as pickle
import xgboost as xgb
logging.config.fileConfig("log.conf")
logger = logging.getLogger("example")

class Model():
    def read(self):
        dtrain = xgb.DMatrix("train.buffer")
        dtest = xgb.DMatrix("test.buffer")
        evallist  = [(dtest,'eval'), (dtrain,'train')]
        num_round = 450
        self._train(dtrain,dtest,evallist,num_round,"XY",True,[],[],2)

    def train(self, X_train, y_train, X_test, ids_test, y_test, outfile, is_valid):
        dtrain = xgb.DMatrix( X_train, label=y_train)
        #dtrain.save_binary("train.buffer")
        dtest = xgb.DMatrix( X_test, missing = -999.0, label=y_test )
        #dtest.save_binary("test.buffer")
        if is_valid:
            evallist  = [(dtest,'eval'), (dtrain,'train')]
        else:
            evallist  = [(dtrain,'train')]
        num_round = 1
        if is_valid:
            self._train(dtrain,dtest,evallist,num_round,outfile,is_valid,ids_test,y_test,2)
        else:
            for i in range(10):
                self._train(dtrain,dtest,evallist,num_round,outfile,is_valid,ids_test,y_test,i)
    def write_evals(self, plst, evals_result):
        fx = []
        klost = ["max_depth","silent","objective","seed","eval_metric","nthread"]
        for (k,v) in plst:
            if k in klost:
                continue
            fx.append(k[0:3]+k[-1]+":"+str(v))
        fx = "|".join(fx)
        fout = open("evals/" + fx, "w")
        for (k,v) in evals_result.items():
            fout.write("%s\t%s\n" % (k,",".join(v)))
        fout.close()

    def add(self, key, vs, default, param, plsts):
        for v in vs:
            param[key] = v
            plst = param.items()
            plsts.append(plst)
        param[key] = default

    def _train(self, dtrain,dtest,evallist,num_round,outfile,is_valid,ids_test,y_test,seed):
        param = {'max_depth':10, "min_child_weight":6, "subsample":0.8, 'eta':0.03,
                'silent':1, 'objective':'binary:logistic',"lambda":5,"gamma":10,
                "colsample_bytree":0.6,"seed":seed}
        param['nthread'] = 4
        plsts = []
        #cole:0.4|mint:6|sube:0.9|etaa:0.03|gama:15|lama:5
        self.add("min_child_weight", [6,3,10], 6, param, plsts)
        self.add("eta", [0.02,0.04,0.05], 0.03, param, plsts)
        self.add("lambda", [2,6,8],5, param, plsts)
        self.add("gamma", [5, 10,15,20], 15, param, plsts)
        for plst in plsts:
            plst += [('eval_metric', 'auc')] # Multiple evals can be handled in this way
            print plst
            sys.stdout.flush()
            evals_result={}
            bst = xgb.train( plst, dtrain, num_round, evallist, evals_result=evals_result)
            self.write_evals(plst, evals_result)
        #evals_result  = bst.get_fscore()
        return []

if __name__ == "__main__":
    model = Model()
    model.read()
