import pandas as pd


df_orig = pd.read_csv('songs_normalize.csv')
df_playlists = pd.read_csv('new_data_playlists.csv')

df = pd.concat([df_orig, df_playlists])

for year in range(2000, 2020):
    name = "new_date_albums_up_to" + str(year)
    df_year = pd.read_csv(name)
    df = pd.concat([df, df_year])

df.drop_duplicates()
print(df.shape)

df.to_csv('big_dataset.csv', index=False)
