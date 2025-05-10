# Import general libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import local libraries
import modules.header as hdr
import modules.functions as func

# Create dataframes from local libraries
text_df = hdr.text_df.loc[hdr.text_df['SourceIDs'].notna()].copy()

# Create reference variable
text_ref_dict = func.get_ref_dict(hdr.text_references.copy())
text_df['Reference'] = [text_ref_dict[x] for x in text_df['ID']]

home_df = text_df.loc[hdr.text_df['Page']=='home'].copy()