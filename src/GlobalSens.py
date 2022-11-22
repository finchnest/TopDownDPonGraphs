from BFS import BFS
import pandas as pd
import utils

def compute_global_sens(filePath, norm, appArgs, method='count'):
    assert norm in ['l1', 'l2']
    vis_attributes = ['user_id', 'public', 'completion_percentage', 'gender', 'last_login',
                  'age', 'body', 'I_am_working_in_field', 'spoken_languages', 'hobbies',
                  'region_large', 'region_small', 'height', 'weight']

    missing = utils.load_missing()
    df = pd.read_csv(filePath)
    graph = utils.create_network(df, vis_attributes, 20000, missing)

    ds_origin = BFS(graph, appArgs)
    original_query = len(ds_origin)

    if method == 'count':
        return int(original_query > 0)

    assert False, 'Untested and slow'
    """
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
    """