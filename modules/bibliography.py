# Import general libraries
import numpy as np
import pandas as pd

# Import local libraries
import modules.header as hdr
import modules.about_the_prisons_prep as pp

src_df = hdr.src_df.copy()
loc_df = hdr.loc_df.copy()
prison_df = hdr.prison_df.copy()
men_df = hdr.men_df.loc[hdr.men_df['SourceIDs'].notna()].copy()
names_df = hdr.men_df.loc[:,['First Name','Last Name']].copy()
text_df = hdr.text_df.copy()

loc_list = pp.loc_list

# Create Reference numbers
src_df_sorted = src_df.sort_values('Bibliographic Reference').copy()
src_df_sorted['Reference'] = src_df_sorted.groupby('Bibliographic Reference').ngroup() + 1

references = src_df_sorted.copy()
references.to_csv('data/references.csv', index=False)

# Create long form source ID tables for the stories from prisons
prison_df['SourceIDs'] = prison_df['SourceIDs'].astype('str')

story_ids = []
src_ids = []

for idx, row in prison_df.iterrows():
    src_arry = row['SourceIDs'].split(',')
    for i in src_arry:
        story_ids.append(row['ID'])
        src_ids.append(i)

prison_src_lf = pd.DataFrame({'ID':story_ids,
                        'SourceID':src_ids}).copy()
prison_src_lf['SourceID'] = prison_src_lf['SourceID'].astype('Int64')

# Create long form source ID tables for the men
men_df['SourceIDs'] = men_df['SourceIDs'].astype('string')

men_ids = []
src_ids = []

for idx, row in men_df.iterrows():
    src_arry = row['SourceIDs'].split(',')
    for i in src_arry:
        men_ids.append(row['ID'])
        src_ids.append(i)

men_src_lf = pd.DataFrame({'ID':men_ids,
                        'SourceID':src_ids}).copy()
men_src_lf['SourceID'] = men_src_lf['SourceID'].astype('Int64')

# Create long form source ID tables for app text
text_df['SourceIDs'] = text_df['SourceIDs'].astype('str')

text_ids = []
src_ids = []

for idx, row in text_df.iterrows():
    src_arry = row['SourceIDs'].split(',')
    for i in src_arry:
        text_ids.append(row['ID'])
        src_ids.append(i)

text_src_lf = pd.DataFrame({'ID':text_ids,
                        'SourceID':src_ids}).copy()
text_src_lf['SourceID'] = text_src_lf['SourceID'].astype('Int64')

# Merge content datasets with sources
src_loc_merged = pd.merge(src_df_sorted, loc_df.loc[loc_df['Location'].isin(loc_list)], on='SourceID', how='left').copy()
src_men_merged = pd.merge(src_df_sorted, men_src_lf, on='SourceID', how='left').copy()
src_prison_merged = pd.merge(src_df_sorted, prison_src_lf, on='SourceID', how='left').copy()
src_text_merged = pd.merge(src_df_sorted, text_src_lf, on='SourceID', how='left').copy()

# Create Reference lists to replace source id lists for prison and men accounts
prison_references = pd.merge(prison_src_lf, src_df_sorted, on='SourceID', how='left').copy()
prison_references.to_csv('data/prison_references.csv', index=False)

men_references = pd.merge(men_src_lf, src_df_sorted, on='SourceID', how='left').copy()
men_references.to_csv('data/men_references.csv', index=False)

text_references = pd.merge(text_src_lf, src_df_sorted, on='SourceID', how='left').copy()
text_references.to_csv('data/text_references.csv', index=False)