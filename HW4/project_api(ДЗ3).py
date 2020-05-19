
# # Creating a GET request
# url = "http://hotline.whalemuseum.org/api.json"
# r = requests.get(url)
# json_obj = r.content.decode("utf-8")
# # Store json data for future reference
# WhalesData = json.loads(json_obj)
#
# # 2. GBIF API
# # GBIF API refers to a data download from the website
# # it is now stored in gbif.csv file.
#
#
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

with open('gbif.csv', 'r') as read_obj:
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
#     for line in csv_reader:
#         print(line)

# # print(WhalesData)
# with open("whales.json", "w") as file:
#     json.dump(WhalesData, file)



import csv, os

with open('edited_gbif.csv', 'r') as f, open('temp.csv', 'w', newline='') as outf:
    csv_reader = csv.DictReader(f, delimiter="\t")
    fields = ["gbifID", "datasetKey", "occurrenceID", "kingdom", "phylum", "class", "order", "family", "genus",
              "species", "taxonRank", "scientificName", "verbatimScientificName", "verbatimScientificNameAuthorship",
              "countryCode", "locality", "stateProvince", "publishingOrgKey", "decimalLatitude", "decimalLongitude",
              "eventDate", "day", "month", "year", "taxonKey", "speciesKey", "basisOfRecord", "institutionCode",
              "collectionCode", "catalogNumber", "dateIdentified", "license", "recordedBy", "lastInterpreted", "issue",
              "sex", "fertility_status", "age", "infant(ADDL)", "safety", "special_needs"]
    writer = csv.DictWriter(outf, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    for line in csv_reader:
        print(line['gbifID'])
        pass
        line["taxonRank"] = 'SPECIES'
        line["locality"] = 'W Reserve of Biosphere'
        line["special_needs"] = list()
        if float(line["age"])<=0.5:
            line["special_needs"].append("Newborn")
        if line["fertility_status"] == "recently_given_birth":
            line["special_needs"].append("Afterbirth care")
        if line["infant(ADDL)"] == "INFANT" and line["sex"] == "Female":
            line["fertility_status"] = "INACTIVE"
        if line["order"] == "Primates":
            line["safety"] = "RELATIVELY_DANGEROUS"
            if line["infant(ADDL)"] == "INFANT":
                line["safety"] = "SAFE"
            if line["fertility_status"] == "recently_given_birth":
                line["safety"] = "DANGEROUS"
        elif line["order"] == "Carnivora":
            if line["infant(ADDL)"] == "INFANT":
                line["safety"] = "RELATIVELY_DANGEROUS"
            else:
                line["safety"] = "DANGEROUS"
        else:
            line["safety"] = "SAFE"

        writer.writerow({"gbifID":line["gbifID"], "datasetKey":line["datasetKey"], "occurrenceID":line["occurrenceID"], "kingdom":line["kingdom"], "phylum":line["phylum"], "class":line["class"], "order":line["order"], "family":line["family"], "genus":line["genus"],
              "species":line["species"], "taxonRank":line["taxonRank"], "scientificName":line["scientificName"], "verbatimScientificName":line["verbatimScientificName"], "verbatimScientificNameAuthorship":line["verbatimScientificNameAuthorship"],
              "countryCode":line["countryCode"], "locality":line["locality"], "stateProvince":line["stateProvince"], "publishingOrgKey":line["publishingOrgKey"], "decimalLatitude":line["decimalLatitude"], "decimalLongitude":line["decimalLongitude"],
              "eventDate":line["eventDate"], "day":line["day"], "month":line["month"], "year":line["year"], "taxonKey":line["taxonKey"], "speciesKey":line["speciesKey"], "basisOfRecord":line["basisOfRecord"], "institutionCode":line["institutionCode"],
              "collectionCode":line["collectionCode"], "catalogNumber":line["catalogNumber"], "dateIdentified":line["dateIdentified"], "license":line["license"], "recordedBy":line["recordedBy"], "lastInterpreted":line["lastInterpreted"], "issue":line["issue"],
              "sex":line["sex"], "fertility_status":line["fertility_status"], "age":line["age"], "infant(ADDL)":line["infant(ADDL)"], "safety":line["safety"], "special_needs":line["special_needs"]})

os.remove('edited_gbif.csv')
os.rename('temp.csv', 'edited_gbif.csv')
with open("edited_gbif.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter="\t")





# Changing primates and pantheras safety status:
import pandas as pd
df = pd.read_csv('input.csv', delim_whitespace=True)
