import pandas as pd
import random
from src import noise
import matplotlib.pyplot as plt
import numpy as np

# df = pd.read_csv('./data/target_data.csv')



df = pd.read_csv('test.csv')
del df['Unnamed: 0']
cols = list(df.columns)
# cols.remove('last_login')
# cols.remove('registration')
# cols.remove('user_id')
# cols.remove('completion_percentage')
# cols.remove('I_am_working_in_field')
# cols.remove('hobbies')
# cols.remove('height')
# cols.remove('weight')
# cols.remove('public')
# cols.remove('region')
# cols.remove('body')
# cols.remove('age')
# cols.remove('spoken_languages')

# counts = df.groupby(list(df.columns)).size()
# count_df = counts.to_frame()
# counts.to_csv('counts.csv', index=False)

# print(df.head())


def add_noise_to_hist(df):

    hist = df.groupby(list(df.columns)).size().reset_index(name='count')
    counts = list(hist['count'])
    sampled_noise = [noise.sample_dgauss(0.5) for _ in counts]
    noisy_counts = []
    noisy_counts_pp = []

    # sampling noise and add to count, also change the negative count to 0(equals to drop)
    for i in range(len(counts)):
        nc = counts[i] + sampled_noise[i]
        noisy_counts.append(nc) # no post-processing (containing negative counts)
        if nc < 0:
            nc = 0
        noisy_counts_pp.append(nc) # with post-processing (no negative counts)
    
    # iterating over noisy_counts and try to add or remove count randomly until the sum of noisy_counts equals to sum(counts)
    noisy_counts_exact = noisy_counts
    noisy_counts_pp_exact = noisy_counts_pp
    while(sum(noisy_counts_exact) != sum(counts)):
        i = random.randint(0, len(noisy_counts_exact)-1)
        if noisy_counts_exact[i] > 0:
            if sum(noisy_counts_exact) > sum(counts):
                noisy_counts_exact[i] -= 1
            elif sum(noisy_counts_exact) < sum(counts):
                noisy_counts_exact[i] += 1

    step = 0    
    while(sum(noisy_counts_pp_exact) != sum(counts)):
        step += 1
        i = random.randint(0, len(noisy_counts_pp_exact)-1)
        if noisy_counts_pp_exact[i] > 0:
            if sum(noisy_counts_pp_exact) > sum(counts):
                noisy_counts_pp_exact[i] -= 1
            elif sum(noisy_counts_pp_exact) > sum(counts):
                noisy_counts_pp_exact[i] += 1

    # add new data to dataframe
    hist['noise_count'] = noisy_counts
    hist['noise_count_pp'] = noisy_counts_pp
    hist['noise_count_pp_exact'] = noisy_counts_pp_exact
    hist['noise_count_exact'] = noisy_counts_exact
    return hist


def find_count(df, col, attr='anony_hobby'):
    
    # only consider some values in the attribute (if considering all, then it won't fit in the figure)
    if attr == 'anony_hobby':
        good_h = [ 'sleeping', 'reading', 'dance', 'games', 'sports', 'movies', 'party', 'swim', 'traveling', 'music']
    elif attr == 'anony_height':
        good_h = ['13X', '14X', '15X', '16X', '17X', '18X', '19X', '20X', '21X']
    elif attr == 'anony_weight':
        good_h = ['3X', '4X', '5X', '6X', '7X', '8X', '9X', '10X', '11X', '12X']
    elif attr == 'anony_age':
        good_h = ['0X', '1X', '2X', '3X', '4X', '5X', '6X', '7X', '8X', '9X']

    # checking whether the value is in good_h
    data = {}
    for i, row in df.iterrows():
        h = str(row[attr])
        if h in good_h:
            if h in list(data.keys()):
                data[h] += int(row[col])
            else:
                data[h] = int(row[col])
    return data

def make_cumulative(df, attr):

    all_data = []
    for c in ['count', 'noise_count', 'noise_count_pp', 'noise_count_exact', 'noise_count_pp_exact']:
        all_data.append(find_count(df, c, attr))
    vals = []

    # transform data into compatible format for histograms plot
    for i, d in enumerate(all_data):    
        val = []
        x = list(all_data[i].keys())
        y = list(all_data[i].values())
        for j, k in enumerate(x):
            for _ in range(y[j]):
                val.append(k)
        vals.append(val)
    
    # do plot
    fig, ax = plt.subplots()
    counts, edges, bars = ax.hist(vals, label=['count', 'noise_count', 'noise_count_pp', 'noise_count_exact', 'noise_count_pp_exact'], linewidth=2, orientation='horizontal')
    for b in bars:
        ax.bar_label(b, fontsize=6)

    plt.xticks(rotation=45, fontsize=8)
    plt.ylabel('counts')
    plt.legend(loc='best')
    plt.title(f'{attr}Count.png')
    plt.savefig(f'./TDA_{attr}.png')

attrs = ['anony_hobby', 'anony_height', 'anony_weight', 'anony_age']
attrs = ['anony_hobby']
with_noise = add_noise_to_hist(df)

# for attr in attrs:
#     make_cumulative(with_noise, attr)

def noise_visualization():

    epsilons = np.arange(0.1, 10.1, 0.01)
    dif = []
    lap = []
    for e in epsilons:
        n = 0
        ll = 0
        for _ in range(10):
            sigma = (2*np.log(1.25/1))/(e**2)
            n += abs(noise.sample_dgauss(sigma))
            ll += abs(noise.sample_dlaplace(1/e))
        n = n/10
        ll = ll/10
        dif.append(n)
        lap.append(ll)

    plt.plot(epsilons, dif, label='discrete gaussian', alpha=0.3)
    plt.plot(epsilons, lap, label='discrete laplace', alpha=0.3)
    plt.ylabel('error')
    plt.xlabel('epsilon')
    plt.legend()
    plt.title('noise')
    plt.savefig('epsilons.png')


df = pd.read_csv('data/target_data.csv')
user_id = df['user_id'].tolist()
new_df = pd.read_csv('./test.csv')
new_df['user_id'] = user_id
new_df.rename(columns = {'anony_hobby':'hobbies' , 'anony_height':'height', 'anony_weight': 'weight', 'anony_age':'age', 'Unnamed: 0':'index'}, inplace = True)
new_df.to_csv('./data/anonymized_data.csv', index=False)

# df = pd.read_csv('better_data.csv')

# # anony_age = []

# # for i, row in df.iterrows():
# #     if int(row['age']) == 0 or int(row['age']) > 90:
# #         df.iloc[i]['age'] = random.randint(12, 40)
    
# #     if int(row['age']) <= 10:
# #         age = '0X'
# #     else:
# #         age = str(row['age'])
# #         age = age[0] + 'X'
# #     anony_age.append(age)

# # df.to_csv('better_data.csv', index=False)

# anony_w = []

# for i, row in df.iterrows():

#     value = row['weight'].replace('kg', '')
#     value = value.replace('and', '')
#     value = value.replace(',', '')
#     value = value.replace('cm', '')
#     value = value.replace(' ', '')
#     if value.isdigit():
#         value = int(value)
#     else:
#         value = random.randint(50, 80)

#     if value < 0:
#         value = random.randint(50, 80)
    
#     if value <= 10:
#         w = '0X'
#     else:
#         w = str(value)
#         w = w[:-1] + 'X'
#     anony_w.append(w)

# anony_h = []
# print('height')
# for i, row in df.iterrows():

#     value = row['height'].replace('cm', '')
#     value = value.replace('cmand', '')
#     value = value.replace(',', '')
#     value = value.replace(' ', '')
#     if value.isdigit():
#         value = int(value)
#     else:
#         value = random.randint(160, 180)

#     if value < 0:
#         value = random.randint(160, 180)
#     if value <= 10:
#         h = '0X'
#     else:
#         h = str(value)
#         h = h[:-1] + 'X'
#     anony_h.append(h)

# new_hobby = []
# for i, row in df.iterrows():

#     value = str(row['hobbies'])
#     values = value.split(', ')
#     value = random.choice(values)

#     if 'web' in values:
#         value = 'internet'
#     if 'sleep' in values:
#         value = 'sleeping'
#     if 'read' in values:
#         value = 'reading'
#     if 'danc' in values:
#         value = 'dance'
#     if 'gam' in values:
#         value = 'games'
#     if 'sport' in value:
#         value = 'sports'
#     if 'movie' in value or 'cinema' in value:
#         value = 'movies'
#     if 'part' in value:
#         value = 'party'
#     if 'swim' in value:
#         value = 'swim'
#     if 'travel' in value:
#         value = 'traveling'
#     if 'music' in value:
#         value = 'music'
#     if len(value) > 15 or len(value) <=3 :
#         value = random.choice(['sports', 'music', 'movies', 'swim', 'traveling', 'party', 'reading', 'games'])
    

#     new_hobby.append(value)

# df['anony_weight'] = anony_w
# df['anony_height'] = anony_h
# df['anony_hobby'] = new_hobby

# df.to_csv('better_data2.csv', index=False)

# col = list(df.columns)
# col.remove('user_id')
# col.remove('last_login')
# col.remove('registration')
# col.remove('region')
# col.remove('body')
# col.remove('I_am_working_in_field')
# col.remove('hobbies')
# col.remove('completion_percentage')
# col.remove('age')
# col.remove('height')
# col.remove('weight')
# col.remove('public')

# df2 = df[col]

# # print(df2.columns)
# c = df2.value_counts()
# print(c.head())