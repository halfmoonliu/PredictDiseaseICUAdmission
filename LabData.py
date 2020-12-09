
import numpy as np
import pandas as pd
import re
import sys
import Libraries




def LabData(Cohort, LabExam):
    '''
    The function takes four dataframes as input, 
    1. Patient Cohort for identifying comorbid conditions
    2. Lab Exam Results

    The function returns a dataframe of AdmissionID and ComorbidCondition1~5, one hot encoded
    '''
    print("Start selecting lab exam results of the cohort....")
    

    CohortGroupAdmissionDateTime = Cohort[['AdmissionID', 'FirstDayICU', 'AdmissionDateTime']]

    CohortExam = pd.merge(CohortGroupAdmissionDateTime, LabExam, how  = 'inner', on = 'AdmissionID')
    CohortExam['AdmissionDateTime']= pd.to_datetime(CohortExam['AdmissionDateTime'])
    CohortExam['ReportDateTime']= pd.to_datetime(CohortExam['ReportDateTime'])
    
    
    CohortExam['AdmissionToReportDay'] = ((CohortExam['ReportDateTime'] - CohortExam['AdmissionDateTime'])) / np.timedelta64(1, 'D')
    
    print("Start extracting selective lab exam results reported between admission minus 3 days and plus one day")
    CohortExam_Selected = CohortExam.loc[(CohortExam['ExamType'].isin(['LabItemA', 'LabItemB', 'LabItemC', 'Pathogen Isolation', 'Pathogen A Sreening'])) & 
                                         (CohortExam['AdmissionToReportDay']>=-3) & (CohortExam['AdmissionToReportDay']<=1)].sort_values(by=['AdmissionID', 'ReportDateTime'], ascending=True)
    
    
    LabExamOneHot_list = list()
    Cohort_AdmissionID_list = CohortGroupAdmissionDateTime['AdmissionID'].unique().tolist()
    #Get initial record for Lab item A, B and C
    for AdmissionID in Cohort_AdmissionID_list:
        LabExamOneHot_AccountID_list = [AdmissionID]
        CohortExam_Selected_AdmissionID = CohortExam_Selected.loc[CohortExam_Selected['AdmissionID']==AdmissionID]
        try:
            LabExamOneHot_AccountID_list.append(CohortExam_Selected_AdmissionID.loc[CohortExam_Selected_AdmissionID['ExamType']=='LabItemA']['ExamResult'].tolist()[0])
        except:
            LabExamOneHot_AccountID_list.append(None)
        try:
            LabExamOneHot_AccountID_list.append(CohortExam_Selected_AdmissionID.loc[CohortExam_Selected_AdmissionID['ExamType']=='LabItemB']['ExamResult'].tolist()[0])
        except:
            LabExamOneHot_AccountID_list.append(None)        
        try:
            LabExamOneHot_AccountID_list.append(CohortExam_Selected_AdmissionID.loc[CohortExam_Selected_AdmissionID['ExamType']=='LabItemC']['ExamResult'].tolist()[0])
        except:
            LabExamOneHot_AccountID_list.append(None)
        #If there is any positive result for pathogen A within the valu
        PathogenA = False
        PathogenIsolationResult_list = CohortExam_Selected_AdmissionID.loc[CohortExam_Selected_AdmissionID['ExamType']=='Pathogen Isolation']['ExamResult'].tolist()
        for PathogenIsolationResult in PathogenIsolationResult_list:
            PathogenIsolationResult_lower = PathogenIsolationResult.lower()
            if re.match(r'.*path.*\ba\b.*', PathogenIsolationResult_lower):
                PathogenA = True
        PathogenAScreeningResult_list = CohortExam_Selected_AdmissionID.loc[CohortExam_Selected_AdmissionID['ExamType']=='Pathogen A Sreening']['ExamResult'].tolist()
        for PathogenAScreeningResult in PathogenAScreeningResult_list:
            PathogenAScreeningResult_lower = PathogenAScreeningResult.lower()
            if re.match(r'.*pos.*', PathogenAScreeningResult_lower):
                PathogenA = True    
                
        if PathogenA == True:
            LabExamOneHot_AccountID_list.append(1)
        else:
            LabExamOneHot_AccountID_list.append(0)            
        LabExamOneHot_list.append(LabExamOneHot_AccountID_list)
    LabExamOneHot_AccountID_df = pd.DataFrame(LabExamOneHot_list, columns = ['AdmissionID', 'LabItemA', 'LabItemB', 'LabItemC', "PathogenA"])
    CohortGroup = Cohort[['AdmissionID', 'FirstDayICU']]
    LabExamOneHot_AccountID_df = pd.merge(CohortGroup, LabExamOneHot_AccountID_df, how = 'left', on = 'AdmissionID')

    
    LabExamOneHot_AccountID_df = LabExamOneHot_AccountID_df.astype({'LabItemA': float, 'LabItemB': float, 'LabItemC': float})
    

    LabExamOneHot_AccountID_df_FirstDayICU = LabExamOneHot_AccountID_df.loc[LabExamOneHot_AccountID_df['FirstDayICU']=="Y"]
    
    print("Descriptive Statistic of group FirstDayICU:")
    print(LabExamOneHot_AccountID_df_FirstDayICU.describe())


    LabExamOneHot_AccountID_df_NotFirstDayICU = LabExamOneHot_AccountID_df.loc[LabExamOneHot_AccountID_df['FirstDayICU']=="N"]
    print("Descriptive Statistic of group FirstDayICU:")
    print(LabExamOneHot_AccountID_df_NotFirstDayICU.describe())
    
    
    
    return LabExamOneHot_AccountID_df
