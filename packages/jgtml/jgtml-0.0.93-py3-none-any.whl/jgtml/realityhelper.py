import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from jgtutils.jgtconstants import MFI_VAL,MFI_SIGNAL,VOLUME,FDB_TARGET as TARGET
#from jgtpy import mfihelper,JGTCDSSvc as cdssvc
import anhelper as anh
import mxhelper
import mxconstants
import jtc
import pandas as pd


#@STCGoal We Have TTF Data with Lags for the pattern 'ttf_mfis_ao_2407a'
#@STCIssue How are created the TTF ?  How to create them with the lags and smaller Datasets (we dont need full)?

from jgtml.ptottf import read_ttf_csv
#from jgtml import anhelper

from jgtml.mfihelper2 import column_mfi_str_in_dataframe_to_id as convert_mfi_columns_from_str_to_id

from jgtml.mxhelper import _mfi_str_add_lag_as_int as add_mfi_lagging_feature_to_ttfdf

def _pto_get_dataset_we_need_in_here__2407060929(i,t,lag_period=1, total_lagging_periods=5,dropna=True, use_full=True,columns_to_keep=None,columns_to_drop=None):
  #Read Data
  df=read_ttf_csv(i, t, use_full=use_full)
  #Convert the MFI columns from str to id before we add lags
  df=convert_mfi_columns_from_str_to_id(df,t, inplace=True)
  #add lags
  df=add_mfi_lagging_feature_to_ttfdf(df,t,lag_period=lag_period, total_lagging_periods=total_lagging_periods,inplace=True)
  if dropna:
    df.dropna(inplace=True)
  if columns_to_keep:
    df=df[columns_to_keep]
  if columns_to_drop:
    for col in columns_to_drop:
      if col in df.columns:
        df.drop(columns=[col],inplace=True)
    #df.drop(columns=columns_to_drop,inplace=True)
  #columns_to_add_lags_to = mxhelper.get_mfi_features_column_list_by_timeframe(t)
  #ttfdf=anhelper.add_lagging_columns(ttfdf, columns_to_add_lags_to)
  return df
  

def create_pattern_dataset__ttf_mfis_ao_2407a_pto_get_dataset_we_need_in_here__2407060929(i,t,lag_period=1, total_lagging_periods=5,dropna=True, use_full=True,columns_to_keep=None,columns_to_drop=None):
  print("INFO::Requires experimentation with training, testing prediction to select from this what we need in reality to make the model work and predict reality of a signal.")
  return _pto_get_dataset_we_need_in_here__2407060929(i,t,lag_period=lag_period, total_lagging_periods=total_lagging_periods,dropna=dropna, use_full=use_full,columns_to_keep=columns_to_keep,columns_to_drop=columns_to_drop)
