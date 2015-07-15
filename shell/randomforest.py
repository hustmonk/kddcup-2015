#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

import math
from sklearn import linear_model, decomposition, datasets
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation
from sklearn import metrics
from sklearn import ensemble
import logging
import logging.config
import sys
import cPickle as pickle
logging.config.fileConfig("log.conf")
logger = logging.getLogger("example")

class Model():
    def train(self, X_train, y_train, X_test, ids_test, y_test, outfile, is_valid):
        print "run"
        clf = ensemble.RandomForestRegressor(n_estimators = 300, verbose=1, n_jobs = -1)
        #clf = ensemble.GradientBoostingRegressor(verbose=1, init = linear_model.LogisticRegression())
        #clf = ensemble.AdaBoostRegressor(base_estimator = linear_model.LogisticRegression())
        #scores = cross_validation.cross_val_score(clf, X_train, y_train, cv=5)
        #logger.info(scores)
        #print scores
        clf.fit(X_train, y_train)
        #preds = clf.predict(X_test)
        preds = clf.predict(X_test)

        modelFileSave = open('valid.model', 'wb')
        pickle.dump(clf, modelFileSave)
        modelFileSave.close()

        """
        if is_valid:
            roc_auc = metrics.roc_auc_score(y_test, preds)
            logger.info(roc_auc)
            print roc_auc,len(X_train)
        """
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
