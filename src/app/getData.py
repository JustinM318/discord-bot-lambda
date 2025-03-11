import pandas as pd
import requests

#     df = pd.read_csv(csv_file, dtype= {
#         'PokedexNumber': str,
#         'name': str,
#         'rarirty': str,
#         'collection': str,
#         'type': str,
#         'stage': str,
#         'description': str
#     })
#     conn = sqlite3.connect(db_file)
#     df.to_sql('cards', conn, if_exists='replace', index=False)
#     conn.close()
    
# Create the database from the CSV file (run this once)
# create_db_from_csv('cards.csv', 'cards.db')

pic_url='https://img.game8.co/3998332/91c4f79b2b3b4206205bf69db8dd3d1e.png/show'
data=requests.get(pic_url)   # read image
photo=data.content
print(photo)