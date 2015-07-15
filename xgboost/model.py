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
    def train(self, X_train, y_train, X_test, ids_test, y_test, outfile, is_valid):
        param = {'bst:max_depth':4, "bst:min_child_weight":10, "bst:subsample":0.8, 'bst:eta':0.08, 'silent':1, 'objective':'binary:logistic',"lambda":0.1,"min_child_weight":10,"n_estimators":500,"learning_rate":0.0825 }
        param['nthread'] = 4
        plst = param.items()
        plst += [('eval_metric', 'auc')] # Multiple evals can be handled in this way
        print plst
        sys.stdout.flush()

        dtrain = xgb.DMatrix( X_train, label=y_train)
        dtest = xgb.DMatrix( X_test, missing = -999.0, label=y_test )

        if is_valid:
            evallist  = [(dtest,'eval'), (dtrain,'train')]
        else:
            evallist  = [(dtrain,'train')]
        num_round = 400
        bst = xgb.train( plst, dtrain, num_round, evallist )

        bst.save_model('0001.model')
        preds = bst.predict( dtest )
        if is_valid:
            roc_auc = metrics.roc_auc_score(y_test, preds)
            logger.info(roc_auc)
            print roc_auc,len(y_test)
        fout = open(outfile, "w")
        for i in range(len(ids_test)):
            fout.write("%s,%.3f\n" % (ids_test[i], preds[i]) )
        fout.close()
        if is_valid:
            fout = open(outfile + ".debug", "w")
            for i in range(len(ids_test)):
                fout.write("%s,%.3f,%d\n" % (ids_test[i], preds[i], y_test[i]) )
            fout.close()
        return preds
