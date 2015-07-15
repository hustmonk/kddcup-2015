#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

set -e
python courseStatisticTime.py
python highuser.py

python module.py
python lastday.py
python objweight.py
python transfer.py
python statistic.py
python moreinfo.py

python lastdayfeature.py
python alldayfeature.py
python day_level_feafure.py
python wholesitefeature.py

sh run.sh
