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


from csv import reader, writer
import random
import csv


choice = ["Male", "Male", "Female"]
# For Females:
birth_condition = ["ready_for_fertilization", "recently_given_birth", "EXPECTANT", "INACTIVE", "INACTIVE", "INACTIVE",
                   "INACTIVE"]
# Age list:
age = []
for i in range(10):
    age.append(random.uniform(1.3, 9.8))
    age.append(random.uniform(0.1, 1))
for i in range(3):
    age.append(random.uniform(9.9, 16))
safety = []
for i in range(3):
    safety.append("DANGEROUS")
for i in range(2):
    safety.append("RELATIVELY_DANGEROUS")
for i in range(5):
    safety.append("SAFE")

spec_needs = []
# Наразі залишимо цей список пустим.

with open('edited_gbif.csv', 'r') as read_obj:
    with open('edited_gbif.csv', 'w', newline='') as write_obj:
        csv_reader = reader(read_obj, delimiter="\t")

        csv_writer = writer(write_obj, delimiter="\t")
        #    Read each row of the input csv file as list

        for row in csv_reader:
            # Append the parameter in the row / list
            row.append(random.choice(choice))
            if row[-1] == "Female":
                row.append(random.choice(birth_condition))
            else:
                row.append("   ---   ")

            row.append(round(random.choice(age), 1))

            if row[-1]<1:
                row.append("INFANT")
            else:
                row.append(" --- ")
            row.append(random.choice(safety))
            row.append("---") # special needs

            # Add the updated row / list to the output file
            csv_writer.writerow(row)



# with open("edited_gbif.csv", "r") as csv_file:
#     csv_reader = csv.DictReader(csv_file, delimiter="\t")
#
#     for line in csv_reader:
#         print(line)

# print(WhalesData)
with open("whales.json", "w") as file:
    json.dump(WhalesData, file)