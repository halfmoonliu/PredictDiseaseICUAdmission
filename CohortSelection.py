#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 17:51:36 2020

@author: halfmoonliu
"""

import pandas as pd
import sys
sys.path.insert(0, '/Users/halfmoonliu/Documents/2020/ICUProject')
import Libraries

DischargeDiagnosis_raw = pd.read_excel('/Users/halfmoonliu/Documents/2020/ICUProject/DischargeDiagnosis.xlsx', header =0)

ICDCodeBook = pd.read_excel('/Users/halfmoonliu/Documents/2020/ICUProject/ICDCodebook.xlsx', header =0)

Demographics_raw = pd.read_excel('/Users/halfmoonliu/Documents/2020/ICUProject/Demographics.xlsx', header =0)
DischargeDiagnosis_stacked = Libraries.CombineFinalDiagnosis(DischargeDiagnosis_raw)

DischargeDiagnosisMap = pd.merge(DischargeDiagnosis_stacked, ICDCodeBook, how  = 'inner', left_on = 'DiagnosisCode', right_on = 'PseudoICD')

Cohort_list = DischargeDiagnosisMap.loc[DischargeDiagnosisMap['DiseaseGroup']=='SpecificDisease']['AdmissionID'].unique().tolist()

CohortDemographics = Demographics_raw.loc[Demographics_raw['AdmissionID'].isin(Cohort_list)]

CohortICU = pd.merge(CohortDemographics, )

