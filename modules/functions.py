# Define functions

# Create a dictionary of IDs and formatted bibliographic References related to list of IDs
def get_ref_dict(df):
    df_sorted = df.sort_values(['ID', 'Reference']).copy()
    ref_dict = {}
    for idx, row in df_sorted.iterrows():
        if row['ID'] not in ref_dict:
            ref_dict[row['ID']] = '[' + str(row['Reference']) + ']'
        else:
            ref_dict[row['ID']] = ref_dict[row['ID']] + ',[' + str(row['Reference']) + ']'
    return ref_dict

# Create list of paragraphs with associated bibliographic references
def get_report(df):
    report_list = df['Report'].tolist()
    ref_list = df['Reference'].tolist()

    report_strings=[]
    for i in range(0, len(report_list)):
        report_strings.append(report_list[i] + str(ref_list[i]))
        
    return report_strings