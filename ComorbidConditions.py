# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 17:30:48 2020

@author: halfmoonliu
"""
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, 'C:\Document\GeneratedData')
import Libraries

ICDCodeBook = pd.read_csv(r'C:\Document\GeneratedData\ICDCodebook.csv', header =0)


DischargeDiagnosis_raw = pd.read_csv(r'C:\Document\GeneratedData\DischargeDiagnosis.csv', header =0)

Cohort_raw = pd.read_excel(r'C:\Document\GeneratedData\Cohort_ICU24H.xlsx', header =0)



def ComorbidConditions(DischargeDiagnosis, ICDCodeBook, Cohort):
    '''
    The function takes four dataframes as input, 
    1. Discharge diagnosis of in patients, 
    2. ICD Code Book mapping Pseudo ICD codes and Disease Group
    3. Patient Cohort for identifying comorbid conditions

    The function returns a dataframe of AdmissionID and ComorbidCondition1~5, one hot encoded
    '''
    print("Start selecting cohort with diagnosis of SpecificDisease, sepratting the cohort into patients transfered to ICU or not.")
    DischargeDiagnosis_stacked = Libraries.CombineFinalDiagnosis(DischargeDiagnosis)

    DischargeDiagnosisMap = pd.merge(DischargeDiagnosis_stacked, ICDCodeBook, how  = 'inner', left_on = 'DiagnosisCode', right_on = 'PseudoICD')
    
    ComorbidConditions = DischargeDiagnosisMap.loc[~DischargeDiagnosisMap['DiseaseGroup'].isin(['Others', 'SpecificDisease'])]

    Cohort_Group = Cohort_raw[['AdmissionID']]
    Cohort_AdmissionID_list = Cohort_Group['AdmissionID'].tolist()
    
    Cohort_ComorbidCoditions_list = list()
    for AdmissionID in Cohort_AdmissionID_list:
        ComorbidConditions_AdmissionID = ComorbidConditions.loc[ComorbidConditions['AdmissionID']==AdmissionID]
        ComorbidConditions_AdmissionID_list = ComorbidConditions_AdmissionID['DiseaseGroup'].unique().tolist()
        Cohort_ComorbidCoditions_AccountId_list = [AdmissionID]
        for ComorbidConditionInd in range(5):
            if 'ComorbidCondition'+str(ComorbidConditionInd+1) in ComorbidConditions_AdmissionID_list:
                Cohort_ComorbidCoditions_AccountId_list.append(1)
            else:
                Cohort_ComorbidCoditions_AccountId_list.append(0)
        Cohort_ComorbidCoditions_list.append(Cohort_ComorbidCoditions_AccountId_list)
    
    Cohort_ComorbidCoditions_df = pd.DataFrame(Cohort_ComorbidCoditions_list, columns = ['AdmissionID', 'ComorbidCondition1', 'ComorbidCondition2', 'ComorbidCondition3', 'ComorbidCondition4', 'ComorbidCondition5'])
    
    return Cohort_ComorbidCoditions_df

results = ComorbidConditions(DischargeDiagnosis_raw, ICDCodeBook, Cohort_raw)
results.to_excel(r'C:\Document\GeneratedData\ComorbidConditions.xlsx', sheet_name='Sheet1', index = False) 