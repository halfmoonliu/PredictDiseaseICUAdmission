# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 16:32:56 2020

@author: halfmoonliu
"""
import numpy as np
import pandas as pd
import sys
import Libraries



def CohortSelection(DischargeDiagnosis, ICDCodeBook, Demographics, ICURecord):
    '''
    The function takes four dataframes as input, 
    1. Discharge diagnosis of in patients, 
    2. ICD Code Book mapping Pseudo ICD codes and Disease Group
    3. Demographics, including hospital in out records.
    4. Patient in/out ICU records.
    The function returns a datafrae of patients with groups and hospital inout records.
    '''
    print("Start selecting cohort with diagnosis of SpecificDisease, sepratting the cohort into patients transfered to ICU or not.")
    DischargeDiagnosis_stacked = Libraries.CombineFinalDiagnosis(DischargeDiagnosis)

    DischargeDiagnosisMap = pd.merge(DischargeDiagnosis_stacked, ICDCodeBook, how  = 'inner', left_on = 'DiagnosisCode', right_on = 'PseudoICD')

    Cohort_list = DischargeDiagnosisMap.loc[DischargeDiagnosisMap['DiseaseGroup']=='SpecificDisease']['AdmissionID'].unique().tolist()

    CohortDemographics = Demographics.loc[Demographics_raw['AdmissionID'].isin(Cohort_list)]
    
    CohortDemographics['AdmissionDateTime']= pd.to_datetime(CohortDemographics['AdmissionDateTime'])
    CohortDemographics['Birthdate']= pd.to_datetime(CohortDemographics['Birthdate'])
    CohortDemographics['Age'] = ((CohortDemographics['AdmissionDateTime'] - CohortDemographics['Birthdate'])) / np.timedelta64(1, 'Y')



    #Check FirstDay ICU Here
    CohortDemographicsICU = pd.merge(CohortDemographics, ICURecord, on = 'AdmissionID', how = 'left')
    CohortDemographicsICU['InICUDatetime']= pd.to_datetime(CohortDemographicsICU['InICUDatetime'])
    
    CohortDemographicsICU['AdmissionToICUDays'] = ((CohortDemographicsICU['InICUDatetime'] - CohortDemographicsICU['AdmissionDateTime'])) / np.timedelta64(1, 'D')
    
    FirstDayICUAdmission = CohortDemographicsICU.loc[CohortDemographicsICU['AdmissionToICUDays']<=1]
    FirstDayICUAdmissionID_list = FirstDayICUAdmission['AdmissionID'].unique().tolist()

    def GroupFirstDayICU(AdminID):
        if AdminID in FirstDayICUAdmissionID_list:
            return "Y"
        else:
            return "N"

    CohortDemographics['FirstDayICU'] = CohortDemographics['AdmissionID'].apply(GroupFirstDayICU)    

    CohortDemographics = CohortDemographics[['AdmissionID','FirstDayICU', 'Sex_int','Age','AdmissionDateTime','DischargeDateTime','InHospitalDays', 'Birthdate']]
    
    CohortFirstDayICU = CohortDemographics.loc[CohortDemographics['FirstDayICU']=="Y"]
    print('The Description of Patients with SpecificDisease Entering ICU the first day is:')
    print(CohortFirstDayICU.describe())

    CohortFirstDayNotICU = CohortDemographics.loc[CohortDemographics['FirstDayICU']=="N"]
    print('The Description of Patients with SpecificDisease NOT Entering ICU the first day is:')
    print(CohortFirstDayNotICU.describe())
    return CohortDemographics
