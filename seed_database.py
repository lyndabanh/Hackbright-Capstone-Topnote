"""Script to seed database."""

import os
import json
import crud
import model
import server
import random

os.system('dropdb mycellar')
os.system('createdb mycellar')

model.connect_to_db(server.app)
model.db.create_all()

# Load wine data from JSON file
# with open('data/winemagdata/archive/winemag-data-130k-v2.json') as f:
#     wine_data = json.loads(f.read())

with open('data/test_wine.json') as f:
    wine_data = json.loads(f.read())

# # Load red wine from csv file
# with open('data/archive/Red.csv', newline = '') as csvfile:
#     red_wine_data = csv.DictReader(csvfile)


# Create wines, store them in a list so we can use them to make ratings
wines_in_db = []
for wine in wine_data:
    title, winery, variety, country, description, designation, points, province, region_1, region_2 = (wine['title'],
                                                                                                    wine['winery'],
                                                                                                    wine['variety'],
                                                                                                    wine['country'],
                                                                                                    wine['description'],
                                                                                                    wine['designation'],
                                                                                                    wine['points'],
                                                                                                    wine['province'],
                                                                                                    wine['region_1'],
                                                                                                    wine['region_2'])

    db_wine = crud.create_wine(title, 
                                winery, 
                                variety, 
                                country, 
                                description, 
                                designation, 
                                points, province, 
                                region_1, 
                                region_2)
    
    wines_in_db.append(db_wine)

# # Create 10 users
# names = ['Liam', 'Olivia', 'Noah', 'Emma', 'Oliver', 'Ava', 'Charlotte', 'William', 'Lucas', 'Chloe']

# for nm in names:
#     name = nm
#     email = f'{nm.lower()}@test.com'
#     password = 'test'
#     quote = 'Test funny wine quote.'

#     user = crud.create_user(name, email, password, quote)

# Create users for demo
names = ['Liam', 'Chloe', 'Charlotte', 'Emma']

quotes = ['Wine a little, laugh a lot', 
            'You had me at merlot', 
            'Great minds drink alike', 
            'I make pour decisions', 
            'Here for the right riesling',
            'On cloud wine',
            'Cabernet. More like, caber-yay',
            'Partners in wine',
            'Stop and smell the rosé',
            'No wine left behind']

for nm in names:
    name = nm
    email = f'{nm.lower()}@gmail.com'
    password = 'password'
    quote = random.choice(quotes)
    quotes.pop(quote)

    user = crud.create_user(name, email, password, quote)



