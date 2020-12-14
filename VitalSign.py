# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 17:30:48 2020

@author: halfmoonliu
"""
import numpy as np
import pandas as pd







Cohort_raw = pd.read_excel(r'C:\Document\GeneratedData\Cohort_ICU24H.xlsx', header =0)
VitalSign_raw = pd.read_csv(r'C:\Document\GeneratedData\VitalSign.csv', header =0)


def VitalSign(Cohort, VitalSign):
    '''
    The function takes two dataframes as input, 
    1. Patient Cohort for retriving their vital signs.
    2. Vital sign Raw data.

    The function returns a dataframe of AdmissionID and selected vital signs, one hot encoded
    '''
    print("Start selecting vital signs of the cohort....")
    

    CohortGroupAdmissionDateTime = Cohort[['AdmissionID', 'FirstDayICU', 'AdmissionDateTime']]

    CohortVitalSign = pd.merge(CohortGroupAdmissionDateTime, VitalSign, how  = 'inner', on = 'AdmissionID')
    print(set(CohortVitalSign['VitalSignType']))
    CohortVitalSign['AdmissionDateTime']= pd.to_datetime(CohortVitalSign['AdmissionDateTime'])
    CohortVitalSign['RecordDateTime']= pd.to_datetime(CohortVitalSign['RecordDateTime'])
    
    
    CohortVitalSign['AdmissionToRecordDay'] = ((CohortVitalSign['RecordDateTime'] - CohortVitalSign['AdmissionDateTime'])) / np.timedelta64(1, 'D')
    
    print("Start extracting selective lab exam results reported within plus or minus 24 hours of admission")
    print(set(CohortVitalSign['VitalSignType']))
    CohortVitalSign = CohortVitalSign.loc[(CohortVitalSign['AdmissionToRecordDay']>=-1) & (CohortVitalSign['AdmissionToRecordDay']<=1)].sort_values(by=['AdmissionID', 'VitalSignType', 'RecordDateTime'], ascending=True)
    print(set(CohortVitalSign['VitalSignType']))
    VitalSignItem_list = ['Temperature', 'Breath Rate', 'Pulse', 'Systolic Pressure', 'Diastolic Pressure', 'SpO2']

    
    VitalSignOneHot = CohortVitalSign[['AdmissionID', 'FirstDayICU']].drop_duplicates()
    
    

    for VitalSignItem in VitalSignItem_list:
        CohortVitalSign_Item = CohortVitalSign[CohortVitalSign['VitalSignType']==VitalSignItem]
        
        CohortVitalSignOneHot_Item_list = list()
        for AdminID in set(CohortVitalSign_Item['AdmissionID']):
        
        
            
            CohortVitalSign_Item_AdminID =  CohortVitalSign_Item[CohortVitalSign_Item['AdmissionID']==AdminID]
            AdminID_Item_Value_list = CohortVitalSign_Item_AdminID['VitalSignValue'].tolist()
            AdminID_Item_Ini = AdminID_Item_Value_list[0]
            AdminID_Item_Min = min(AdminID_Item_Value_list)
            AdminID_Item_Max = max(AdminID_Item_Value_list)
            
            CohortVitalSignOneHot_Item_list.append([AdminID, AdminID_Item_Ini, AdminID_Item_Min, AdminID_Item_Max])
            
            
        CohortVitalSignOneHot_Item_df = pd.DataFrame(CohortVitalSignOneHot_Item_list, columns = ['AdmissionID', VitalSignItem + "_INI", VitalSignItem + "_MAX",VitalSignItem + "_MIN"])           
        
        VitalSignOneHot = pd.merge(VitalSignOneHot, CohortVitalSignOneHot_Item_df, how = 'left', on = 'AdmissionID')    
        
    
    
    Selective_Items = ['Temperature_MAX', 'Pulse_MAX',  'Systolic Pressure_MIN', 'Diastolic Pressure_MIN']
    
    
    VitalSignOneHot_FirstDayICU = VitalSignOneHot.loc[VitalSignOneHot['FirstDayICU']=="Y"]
    
    
    print("The Descriptives of Selective Vital Signs of First Day ICU is:")
    
    print(VitalSignOneHot_FirstDayICU.describe())
    for item in Selective_Items:
        print(VitalSignOneHot_FirstDayICU[item].describe())
    VitalSignOneHot_NotFirstDayICU = VitalSignOneHot.loc[VitalSignOneHot['FirstDayICU']=="N"]
    print("The Descriptives of Selective Vital Signs of Not First Day ICU is:")
    for item in Selective_Items:
        print(VitalSignOneHot_NotFirstDayICU[item].describe())
    
    
    
    
    
    return VitalSignOneHot

results = VitalSign(Cohort_raw, VitalSign_raw)

results.to_excel(r"C:\Document\GeneratedData\VitalSignOneHot.xlsx", sheet_name='Sheet1', index = False) 