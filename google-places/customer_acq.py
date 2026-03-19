import requests
from dotenv import load_dotenv
import os
import psycopg2
import csv

load_dotenv()
places_key=os.getenv('key')
sql_key=os.getenv('sql_key')

conn = psycopg2.connect(
    dbname="stockdata",
    user="postgres",
    password=sql_key,
    host="localhost",
    port="5432")

curs = conn.cursor()
curs.execute("CREATE TABLE IF NOT EXISTS lead_database (name TEXT,website_URL TEXT,maps_URL TEXT,address TEXT)")
curs.execute("DELETE FROM lead_database")
conn.commit()

query = ['high rise apartment management company san francisco',
         'residential property management san francisco',
         'luxury apartment property management san francisco',
         'apartment building management company sf,'
         'HOA management san francisco']


def find_place(query:list,key):
    data = []
    base_url = 'https://places.googleapis.com/v1/places:searchText'
    for i in query:
        new_search = requests.post(base_url,
                            headers={'X-Goog-FieldMask':'places.displayName,places.formattedAddress,places.googleMapsUri,places.websiteUri',"X-Goog-Api-Key":key},
                            json={'textQuery':i})
        data.extend(new_search.json()['places'])
    return data


def database_upload(data:dict):
    for i in data:
        curs = conn.cursor()
        curs.execute("INSERT INTO lead_database (name,website_URL,maps_URL,address)"
                    "VALUES (%s,%s,%s,%s)", 
                    (i['displayName']['text'],i.get('websiteUri','N/A'),i['googleMapsUri'],i.get('formattedAddress','N/A')))
        conn.commit()

def export_to_csv():
    with open('lead_database','w') as new:
        writer = csv.writer(new)
        writer.writerow(['Name','Website URL','Google Maps URL','Address'])
        curs.execute("SELECT * FROM lead_database")
        rows = curs.fetchall()
        writer.writerows(rows)

    

database = find_place(query,places_key)
database_upload(database)
export_to_csv()
