import BFS
import utils
import math
import pandas as pd
from RelationalOp import RelationalOp
from tqdm import tqdm

def filter(df, top_key, top_value, med_key, med_value, bot_key, bot_value, low_ops):
    
    if low_ops == RelationalOp.EQUAL:
        df_filtered = df[(df[top_key]==top_value)&(df[med_key]==med_value)&(df[bot_key]==bot_value)]
    elif low_ops == RelationalOp.GREAT_THAN_EQ:
        df_filtered = df[(df[top_key]==top_value)&(df[med_key]==med_value)&(df[bot_key]>=bot_value)]
    elif low_ops == RelationalOp.LESS_THAN_EQ:
        df_filtered = df[(df[top_key]==top_value)&(df[med_key]==med_value)&(df[bot_key]<=bot_value)]
    elif low_ops == RelationalOp.LESS_THAN:
        df_filtered = df[(df[top_key]==top_value)&(df[med_key]==med_value)&(df[bot_key]<bot_value)]
    elif low_ops == RelationalOp.GREAT_THAN:
        df_filtered = df[(df[top_key]==top_value)&(df[med_key]==med_value)&(df[bot_key]>bot_value)]
    return df_filtered


def compute_global_sens(norm, appArgs, method='count'):

    df = pd.read_csv('../data/anonymized_data.csv')
    assert norm in ['l1', 'l2']

    top_key = appArgs.top[0].key
    top_value = appArgs.top[0].value

    med_key = appArgs.med[0].key
    med_value = appArgs.med[0].value

    bot_key = appArgs.bot[0].key
    bot_value = appArgs.bot[0].value
    bot_ops = appArgs.bot[0].relationalOp

    all_diffs = []
    ds_origin = filter(df, top_key, top_value, med_key, med_value, bot_key, bot_value, bot_ops)
    original_query = len(ds_origin)

    if method == 'count':
        if original_query == 0:
            return 0
        else:
            return 1

    for i in tqdm(range(len(df))):
        ds_prime = df.copy().T
        ds_prime.pop(i)
        ds_filtered = test_filter(ds_prime.T, top_key, top_value, med_key, med_value, bot_key, bot_value, bot_ops)
        q = len(ds_filtered)
        dif = abs(q-original_query)
        if norm == 'l2':
            dif = dif*dif
        all_diffs.append(dif)
        
    if norm == 'l1':
        return max(all_diffs)
    else:
        all_diffs = [math.sqrt(dif) for dif in all_diffs]
        return max(all_diffs)