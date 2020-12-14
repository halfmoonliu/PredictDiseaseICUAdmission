# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:56:24 2020

@author: USER
"""


import pandas as pd


Cohort_raw = pd.read_excel(r'C:\Document\GeneratedData\Cohort_ICU24H.xlsx', header =0)

ComorbidConditions_raw = pd.read_excel(r'C:\Document\GeneratedData\ComorbidConditions.xlsx', header =0)
LabExamOneHot_raw = pd.read_excel(r'C:\Document\GeneratedData\ExamOneHot.xlsx', header =0)

VitalSignOneHot_raw = pd.read_excel(r'C:\Document\GeneratedData\VitalSignOneHot.xlsx', header =0)

def FeatureSelection(Cohort, ComorbidCondition, LabExam, VitalSign):
    
    Dataset = Cohort[['AdmissionID', 'FirstDayICU', 'Age', 'Sex_int']]
    
    
    
    #Comorbid Conditions: 'ComorbidCondition1', 'ComorbidCondition2', 'ComorbidCondition3', 'ComorbidCondition4', 'ComorbidCondition5'
    
    ComorbidConditionSelected = ComorbidCondition[['AdmissionID', 'ComorbidCondition1', 'ComorbidCondition2', 'ComorbidCondition3', 'ComorbidCondition4', 'ComorbidCondition5']]
    
    Dataset = pd.merge(Dataset, ComorbidConditionSelected, how = 'left', on = 'AdmissionID')
    #LabExam 'LabItemA', 'LabItemB', 'LabItemC', "PathogenA"
    LabExamSelected = LabExam[['AdmissionID', 'LabItemA', 'LabItemB', 'LabItemC', "PathogenA"]]
    
    Dataset = pd.merge(Dataset, LabExamSelected, how = 'left', on = 'AdmissionID')
    
  
    
    #Vital Sign ['Temperature_MAX', 'Pulse_MAX',  'Systolic Pressure_MIN', 'Diastolic Pressure_MIN'
    VitalSignSelected = VitalSign[['AdmissionID', 'Temperature_MAX', 'Pulse_MAX',  'Systolic Pressure_MIN', 'Diastolic Pressure_MIN']]
    
    Dataset = pd.merge(Dataset, VitalSignSelected, how = 'left', on = 'AdmissionID')    
    
    
    return Dataset

results = FeatureSelection(Cohort_raw, ComorbidConditions_raw, LabExamOneHot_raw, VitalSignOneHot_raw)

results.to_excel(r"C:\Document\GeneratedData\Dataset.xlsx", sheet_name='Sheet1', index = False) 