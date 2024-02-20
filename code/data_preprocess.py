import sys
import pandas as pd 
sys.path.insert(0, '/Users/pooja/Desktop/GitHub/mrdc_model_monitoring/conf')
from config import SQLQuery
from queries import reference_data, current_data

path1 = "/Users/pooja/Desktop/GitHub/mrdc_model_monitoring/data/"
path2 = "/Users/pooja/Desktop/GitHub/mrdc_model_monitoring/reports/"
 
features = ['ach_c_median_past30d', 
            'ach_c_std_past30d',
            'ach_d_avg_past10d',
            'ach_d_median_past30d', 
            'amount', 
            'avg_running_balance_past30d',
            'card_txn_std_past10by30d', 
            'card_txn_std_past10d',
            'credit_txn_avg_past10by30d', 
            'credit_txn_avg_past10d',
            'credit_txn_count_past10by30d', 
            'credit_txn_std_past30d',
            'debit_txn_count_past10by30d', 
            'ein_ssn', 
            'is_between1000and5000',
            'is_between200and1000', 
            'mrdc_c_avg_past30d',
            'mrdc_c_median_past10by30d', 
            'od_count_past30d',
            'past10by30d_between200and1000_ratio', 
            'past10by30d_check_ratio',
            'past10by30d_returned_check_ratio', 
            'pd_avg_past10d',
            'rejected_past10by30d_between200and1000_ratio',
            'returned_past30d_avg_check_amount', 
            'rn_past30d_avg_check_amount',
            'past10by30d_lessthan200_ratio']


def reference_data(): 
    df_ref = pd.read_csv(path1 + 'mrdc_training.csv')
    df_ref.columns = df_ref.columns.str.lower()
    df_ref = df_ref[features]
    return df_ref

def preprocess_cur(df_cur): 
    df_cur = df_cur[features + ['score' , 'status']]
    df_cur = df_cur[(df_cur['status'] == 'returned') | (df_cur['status'] == 'deposited')]
    df_cur.rename(columns={'score': 'predictions'}, inplace = True)
    df_cur['actual_return'] = df_cur['status'].apply(lambda x: 0 if x == 'deposited' else 1 )
    df_cur['probability'] = df_cur['predictions'] / 1000 
    return df_cur

def preprocess_ref():
    df_ref = pd.read_csv(path1 + 'mrdc_training.csv')
    df_ref.columns = df_ref.columns.str.lower() 
    df_ref =  df_ref[(df_ref['status'] == 'returned') | (df_ref['status'] == 'deposited')]
    df_ref = df_ref[features + ['predictions', 'status']]
    df_ref['actual_return'] = df_ref['status'].apply(lambda x: 0 if x == 'deposited' else 1 )
    df_ref['probability'] = df_ref['predictions'] / 1000
    return df_ref


def model_drift(): 
    querySno = SQLQuery('snowflake')
    engine = querySno.engine
    df_cur = querySno(current_data)
    df_cur.fillna(0)
    df_cur = preprocess_cur(df_cur)
    return df_cur

def data_drift(): 
    querySno = SQLQuery('snowflake')
    engine = querySno.engine
    df_cur = querySno(current_data)
    df_cur = df_cur[features]
    df_cur.fillna(0)
    return df_cur 
    