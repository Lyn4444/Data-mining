# -*- coding: utf-8 -*-
# @ProjectName: Datamining
# @File: Analysis.py
# @Author: Lyn
# @Date: 2020/12/1 0:27
# @IDE: PyCharm
# @Version: 1.0
# @Function:

import pandas as pd

df = pd.read_csv(r'test1.csv')
pd.set_option('display.max_rows', 4)

df.info()
