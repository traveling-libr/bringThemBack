# Import general libraries
import pandas as pd
import numpy as np

# Import local libraries
from local.utilities.functions import create_sources_lf, get_ref_dict, get_ref_dict_lnkd, get_report
from local.utilities.data import src_df, loc_df, prison_df, all_men_df, text_df, accounts_df

"""
REFERENCE DATA - CREATE BIBLIOGRAPHY AND REFERENCES
"""
"""
CREATE REFERENCE NUMBERS
"""
src_df_sorted = src_df.sort_values('Bibliographic Reference').copy()
src_df_sorted['Reference'] = src_df_sorted.groupby('Bibliographic Reference').ngroup() + 1

references = src_df_sorted.copy()
#references.to_csv('data_references/references.csv', index=False)

"""
CREATE LONG-FORM SOURCE ID DATASETS - ONE RECORD FOR EACH SOURCE IN SourceIDs
"""
prison_src_lf = create_sources_lf(prison_df)
#prison_src_lf.to_csv('data_references/prison_references.csv', index=False)

men_src_lf = create_sources_lf(all_men_df.loc[all_men_df['SourceIDs'].notna()].copy())
#men_src_lf.to_csv('data_references/men_references.csv', index=False)

accounts_src_lf = create_sources_lf(accounts_df)
#accounts_src_lf.to_csv('data_references/accounts_references.csv', index=False)

text_src_lf = create_sources_lf(text_df)
#text_src_lf.to_csv('data_references/text_references.csv', index=False)

"""
MATCH REFERENCES TO BIBLIOGRAPHIC REFERENCES AND ADD TO DATAFRAMES
"""
prison_ref = pd.merge(prison_src_lf, references, on='SourceID', how='left').copy()
prison_ref_dict = get_ref_dict(prison_ref)
prison_df['Reference'] = [prison_ref_dict[int(x)] for x in prison_df['ID']]
prison_ref_dict_lnkd = get_ref_dict_lnkd(prison_ref)
prison_df['Reference_lnkd'] = [prison_ref_dict_lnkd[int(x)] for x in prison_df['ID']]

men_ref = pd.merge(men_src_lf, references, on='SourceID', how='left').copy()
men_ref_dict = get_ref_dict(men_ref)
all_men_df['Reference'] = [np.nan if str(x)=='nan' else men_ref_dict[int(x)] for x in all_men_df['ID']]
men_ref_dict_lnkd = get_ref_dict_lnkd(men_ref)
all_men_df['Reference_lnkd'] = [np.nan if str(x)=='nan' else men_ref_dict_lnkd[int(x)] for x in all_men_df['ID']]

text_ref = pd.merge(text_src_lf, references, on='SourceID', how='left').copy()
text_ref_dict = get_ref_dict(text_ref)
text_df['Reference'] = [text_ref_dict[int(x)] for x in text_df['ID']]
text_ref_dict_lnkd = get_ref_dict_lnkd(text_ref)
text_df['Reference_lnkd'] = [text_ref_dict_lnkd[int(x)] for x in text_df['ID']]

accounts_ref = pd.merge(accounts_src_lf, references, on='SourceID', how='left').copy()
accounts_ref_dict = get_ref_dict(accounts_ref)
accounts_df['Reference'] = [np.nan if str(x)=='nan' else accounts_ref_dict[int(x)] for x in accounts_df['ID']]
accounts_ref_dict_lnkd = get_ref_dict_lnkd(accounts_ref)
accounts_df['Reference_lnkd'] = [np.nan if str(x)=='nan' else accounts_ref_dict_lnkd[int(x)] for x in accounts_df['ID']]

"""men_ref_lf = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringthemback/refs/heads/main/data_references/men_references.csv')
prison_ref_lf = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringthemback/refs/heads/main/data_references/prison_references.csv')
ref_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringthemback/refs/heads/main/data_references/references.csv')
text_ref_lf = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringthemback/refs/heads/main/data_references/text_references.csv')
accounts_ref_lf = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringthemback/refs/heads/main/data_references/accounts_references.csv')
"""
"""
CREATE REFERENCE VARIABLES AND GROUPS
"""
all_men_df['Age Group'] = ['0-4' if x <= 4 else '5-14' if x <= 14 else '15-24' if x <= 24 else '25-34' if x <= 34 else '35-44' if x <= 44 else '45-54' if x <= 54 else '55-64' if x <= 64 else 'Unknown' for x in all_men_df['Age at Deportation'] ]
all_men_df['Full Name'] = [i + ' ' + j for (i, j) in zip(all_men_df['First Name'], all_men_df['Last Name'])]
all_men_df['Reverse Name'] = all_men_df['Last Name'] + ", " + all_men_df['First Name']

""" 
CREATE DATAFRAME FOR 'CHART SUMMARY'
"""
men_df = all_men_df.loc[all_men_df['SourceIDs'].notna()].copy()

bar_init = {}
bar_init['stat'] = 'All'
bar_init['age'] = 'All'
bar_init['rec'] = 'All'

stat_init = 'All'
stat_dict = {'All':'All'}
for e in sorted(men_df['Immigration Status'].unique().tolist()):
    stat_dict[e] = e

age_init = 'All'
age_dict = {'All':'All'}
for e in sorted(men_df['Age Group'].unique().tolist()):
    age_dict[e] = e

rec_init = 'All'
rec_dict = {'All':'All'}
for e in sorted(men_df['Criminal Record'].unique().tolist()):
    rec_dict[e] = e

bar_dict = {}
bar_dict['stat'] = stat_dict
bar_dict['age'] = age_dict
bar_dict['rec'] = rec_dict

"""
CREATE DATAFRAMES AND VARIABLES FOR 'HOME' AND 'ABOUT'
"""
names_df = all_men_df.loc[:,['First Name', 'Last Name', 'Reverse Name']].sort_values(['Last Name', 'First Name']).copy()
app_text = get_report(text_df, rtype='dict')

"""
INITIALIZE VARIABLES FOR 'THE MEN'
"""
mid_init = 1

section_dict = {'immigration_account':'Immigration Account',
                'family':'Family',
                'criminal_history':'Criminal History'}

"""
CREATE DATASETS AND INITIALIZE VARIABLES FOR 'THE PRISONS'
"""
loc_list = ['All'] + sorted(loc_df['Location'].unique().tolist())
map_init = {}
map_init['loc'] = 'All'
map_init['lat'] = 13.6929
map_init['lon'] = -89.2182

# Merge prison_df with loc_df for content and geographic data for map
map_content_init = pd.merge(prison_df, loc_df, on='Location', how='left').copy()

# Select data only if prison is in loc_df
# Sort by LOCATION ad ORDER to display paragraphs in chosen order for each location
prisons = loc_df.Location.unique().tolist()
map_content_df = map_content_init.loc[map_content_init['Location'].isin(prisons)].sort_values(['Location','Order']).copy()
