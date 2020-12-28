import numpy as np
import pandas as pd
import sys
# Project Libraries
import Libraries
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

