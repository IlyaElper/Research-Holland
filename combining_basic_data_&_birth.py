print('start')
import os
import sqlite3
# import libraries
import pandas as pd
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
print(current_directory)
# load data 
conn = sqlite3.connect('2012_to_2017_deputat_speakers.db')
query = "SELECT * FROM filtered_rows"  
filtered_rows = pd.read_sql(query, conn)
query = "SELECT * FROM speakers_place_of_birth"  
speakers_place_of_birth = pd.read_sql(query, conn)
conn.close()
# combining basic data with places of birth
filtered_rows['speaker_name'] = filtered_rows['speaker_name'].str.title()
merged_df = pd.merge(filtered_rows, speakers_place_of_birth.iloc[:, :-4] , left_on='speaker_name', right_on='speakers', how='left')
# save  to db table df_for_modeling
# Establish connection to the database
conn = sqlite3.connect('2012_to_2017_deputat_speakers.db')
# Save DataFrame to the database
merged_df.to_sql('df_for_modeling', conn, if_exists='replace', index=False)
# speakers_place_of_birth.to_sql('speakers_place_of_birth', conn, if_exists='replace', index=False)
# Close the connection
conn.close()
print('finish')