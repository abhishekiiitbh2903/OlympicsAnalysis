import pandas as pd

def preprocess(df,region_df):
    # filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    temp_df = pd.get_dummies(df['Medal']).astype(int)
    df = pd.concat([df, temp_df], axis=1)
    return df