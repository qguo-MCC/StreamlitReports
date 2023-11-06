import pandas as pd
canmeds = pd.read_csv('data/archive/CanMEDSClusteringFinal.csv')
canmeds['ctid'] = canmeds['cluster_id'].astype(str) +'_'+ canmeds['id'].astype(str)
canmeds.drop_duplicates(subset=['ctid'], ignore_index=True, inplace=True)
c_counts = canmeds['cluster_id'].value_counts()

meded = pd.read_csv('data/archive/MedEdClusteringFinal.csv')
meded['ctid'] = meded['cluster_id'].astype(str) +'_'+ meded['id'].astype(str)
meded.drop_duplicates(subset=['ctid'], ignore_index=True, inplace=True)
meded['cluster_id'].value_counts()
meded = meded.loc[((meded['id']==1547642151034445824)&(meded['cluster_id']==5))==False]
m_counts = meded['cluster_id'].value_counts()

#ctweets = pd.read_csv('data/tweets_classified_cleaned.csv')
#tweets = pd.read_csv('data/tweets.csv')
#users = pd.read_csv('data/user_descriptions.csv')
#cleaders = pd.read_csv('data/CanMEDSInfluencers.csv')
#eleaders = pd.read_csv('data/MedEdInfluencers.csv')

#assert set(canmeds['id'].to_list()).difference(tweets['id'].to_list())
#1) get original leader tweets and user id
#tweets.loc[tweets['id'].isin(canmeds['id'].to_list()),['id', 'text', 'user']]

groups = ['Medical_professional', 'Advocate_Activist', 'Educator', 'Researcher', 'organizations', 'Government', 'Miscellaneous']
cthemes = pd.read_csv('data/archive/CanMEDSThemeFinal.csv')
cthemes['csize_old'] = cthemes['cluster_size']
cthemes['cluster_size'] = cthemes['id'].apply(lambda e: c_counts.loc[e])
for g in groups:
    cthemes[g] = (cthemes['cluster_size']*cthemes[g]/cthemes['csize_old']).round(0)

mthemes = pd.read_csv('data/archive/MedEdThemeFinal.csv')
mthemes['csize_old'] = mthemes['cluster_size']
mthemes['cluster_size'] = mthemes['id'].apply(lambda e: m_counts.loc[e])
for g in groups:
    mthemes[g] = (mthemes['cluster_size']*mthemes[g]/mthemes['csize_old']).round(0)


canmeds.to_csv('data/CanMEDSClusteringFinal.csv', index=False)
meded.to_csv('data/MedEdClusteringFinal.csv', index=False)
canmeds.to_csv('data/CanMEDSThemeFinal.csv', index=False)
canmeds.to_csv('data/MedEdThemeFinal.csv', index=False)


