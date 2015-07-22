#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

set -e
#build info
function runinfo() {
python objweight.py
python courseStatisticTimeInfo.py
python lastdayInfo.py
python courseTimeSequenceInfo.py
python statisticInfo.py
python transfer.py
python userPredictInfo.py
python userStatisticInfo.py
}

function runfeature(){
#build single feature
python baseEnrollmentFeature.py
python lastdayFeature.py
python wholeEnrollmentFeature.py
python baseTimeFeature.py
python userPredictFeature.py
python wholeWebsiteFeature.py
python dayLevelFeature.py
python statisticFeature.py
}
runinfo
runfeature
sh run.sh
