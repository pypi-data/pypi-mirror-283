import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from jgtutils.jgtconstants import MFI_VAL,MFI_SIGNAL,VOLUME,FDB_TARGET as TARGET
from jgtpy import mfihelper
from jgtpy.mfihelper import get_mfi_features_column_list_by_timeframe
import anhelper as anh

import jtc
import pandas as pd
from jgtpy import JGTCDSSvc as cdssvc

#@STCGoal We Have TTF Data with Lags for the pattern 'ttf_mfis_ao_2407a'
#@STCIssue How are created the TTF ?  How to create them with the lags and smaller Datasets (we dont need full)?

def _pto_get_dataset_we_need_in_here__2407060929(i,t):
  from jgtml.ptottf import read_ttf_csv
  ttfdf=read_ttf_csv(i, t, use_full=True)
  from jgtpy.mfihelper import get_mfi_features_column_list_by_timeframe
  columns_to_add_lags_to = get_mfi_features_column_list_by_timeframe(t)
  from jgtml import anhelper
  ttfdf=anhelper.add_lagging_columns(ttfdf, columns_to_add_lags_to)
  

def create_pattern_dataset__ttf_mfis_ao_2407a(i,t,lag_period=1, total_lagging_periods=5,drop_columns_arr = ['BidOpen', 'BidHigh', 'BidLow', 'BidClose', 'AskOpen', 'AskHigh','AskLow', 'AskClose', 'fh13', 'fl13', 'fh21', 'fl21', 'fh34', 'fl34', 'fh55','fl55','price_peak_above', 'price_peak_bellow', 'ao_peak_above','ao_peak_bellow'],dropna_volume=True):
  
  df=_read_mx_and_prep_02(i,t,drop_columns_arr,dropna_volume)
  _mfi_str_add_lag_as_int(df,t,lag_period, total_lagging_periods)
  return df
