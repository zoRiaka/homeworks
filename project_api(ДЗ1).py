# 1. The Whale Hotline API
import requests
import json

# Creating a GET request
url = "http://hotline.whalemuseum.org/api.json"
r = requests.get(url)
json_obj = r.content.decode("utf-8")
# Store json data for future reference
WhalesData = json.loads(json_obj)

# 2. GBIF API
# GBIF API refers to a data download from the website
# it is now stored in gbif.csv file.





