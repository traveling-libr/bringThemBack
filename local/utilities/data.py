# Import general libraries
import pandas as pd

"""
READ CSV - CONTENT DATA
"""
src_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringthemback/refs/heads/main/data/sources.csv')
loc_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringthemback/refs/heads/main/data/locations.csv')
prison_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringthemback/refs/heads/main/data/the_prisons.csv')
all_men_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringthemback/refs/heads/main/data/the_men.csv')
text_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringthemback/refs/heads/main/data/app_text.csv')
accounts_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringthemback/refs/heads/main/data/accounts.csv')