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
import random
class Model():
    def read(self):
        self.random = False
        dtrain = xgb.DMatrix("train.buffer")
        dtest = xgb.DMatrix("test.buffer")
        evallist  = [(dtest,'eval'), (dtrain,'train')]
        num_round = 450
        self._train(dtrain,dtest,evallist,num_round,"XY",True,[],[],2)

    def train(self, X_train, y_train, X_test, ids_test, y_test, outfile, is_valid):
        dtrain = xgb.DMatrix( X_train, label=y_train)
        if is_valid:
            dtrain.save_binary("train.buffer")
        dtest = xgb.DMatrix( X_test, missing = -999.0, label=y_test )
        if is_valid:
            dtest.save_binary("test.buffer")
        if is_valid:
            evallist  = [(dtest,'eval'), (dtrain,'train')]
            self.random = False
        else:
            evallist  = [(dtrain,'train')]
            self.random = True
        num_round = 450
        if is_valid:
            self._train(dtrain,dtest,evallist,num_round,outfile,is_valid,ids_test,y_test,2)
        else:
            for i in range(10):
                self._train(dtrain,dtest,evallist,num_round,outfile,is_valid,ids_test,y_test,i)
    def getrand(self):
        if self.random:
            return random.randint(0,20) - 10
        else:
            return 0
    def _train(self, dtrain,dtest,evallist,num_round,outfile,is_valid,ids_test,y_test,seed):
        #cole:0.4|mint:6|sube:0.9|etaa:0.05|gama:15|lama:5 0.897681 0.897757
        #cole:0.6|mint:6|sube:0.8|etaa:0.03|gama:10|lama:6
        #cole:0.6|mint:6|sube:0.8|etaa:0.03|gama:10|lama:6 0.898634 0.898749 0.898597
        #cole:0.4|mint:6|sube:0.9|etaa:0.03|gama:15|lama:2 0.899914 0.899939
        param = {'max_depth':100, "min_child_weight":6, "subsample":0.89+self.getrand()*0.005,
                    'eta':0.03+self.getrand()*0.001, 'silent':1, 'objective':'binary:logistic',
                    "lambda":4+self.getrand()*0.1,"gamma":14+self.getrand()*0.2,
                    "colsample_bytree":0.4+self.getrand()*0.01,"seed":seed,
                    'nthread':4,'eval_metric':'auc'}
        plst = param.items()
        print plst
        sys.stdout.flush()
        evals_result={}
        bst = xgb.train( plst, dtrain, num_round, evallist, evals_result=evals_result)
        preds = bst.predict( dtest )
        #evals_result  = bst.get_fscore()`
        """
        fout = open("evals/evals_result", "w")
        for (k,v) in evals_result.items():
            fout.write("%s\t%s\n" % (k,v))
        fout.close()
        """
        if is_valid == False :
            fout = open("merge/"+outfile+str(seed), "w")
            for i in range(len(ids_test)):
                fout.write("%s,%.3f\n" % (ids_test[i], preds[i]) )
            fout.close()
        return preds

if __name__ == "__main__":
    model = Model()
    model.read()
