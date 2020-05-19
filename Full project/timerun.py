import csv, os

import random

def check_heartbeat(norm):
    """return True if sensor in norm"""
    low = int(norm[0])
    high = int(norm[1])
    chances = [i for i in range(low-2, high+4)]
    generated_heartb = random.choice(chances)
    if generated_heartb <= high and generated_heartb >= low:
        return True
    else:
        return False

def check_pressure(norm):
    """return True if sensor in norm"""
    chance = random.random()
    if chance<= 0.2:
        return False
    else:
        return True
def check_oxygen(norm):
    """return True if sensor in norm"""
    low = int(norm[0])
    high = int(norm[1])
    chances = [i for i in range(low - 2, high + 4)]
    generated_oxg = random.choice(chances)
    if generated_oxg <= high and generated_oxg >= low:
        return True
    else:
        return False
def get_longitude():
    lowest = 2.4
    heighest = 3.07
    return round(random.uniform(lowest, heighest), 5)
def get_latitude():
    lowest = 11.6
    heighest = 12.1
    return round(random.uniform(lowest, heighest), 5)

def rewrite(anim_list):
    with open('edited_gbif.csv', 'r') as f, open('temp.csv', 'w', newline='') as outf:
        csv_reader = csv.DictReader(f, delimiter="\t")
        fields = ["gbifID", "datasetKey", "occurrenceID", "kingdom", "phylum", "class", "order", "family", "genus",
                  "species", "taxonRank", "scientificName", "verbatimScientificName",
                  "verbatimScientificNameAuthorship",
                  "countryCode", "locality", "stateProvince", "publishingOrgKey", "decimalLatitude", "decimalLongitude",
                  "eventDate", "day", "month", "year", "taxonKey", "speciesKey", "basisOfRecord", "institutionCode",
                  "collectionCode", "catalogNumber", "dateIdentified", "license", "recordedBy", "lastInterpreted",
                  "issue",
                  "sex", "fertility_status", "age", "infant(ADDL)", "safety", "special_needs"]
        writer = csv.DictWriter(outf, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        i = 0
        for line in csv_reader:
            for anm in anim_list:
                writer.writerow(
                    {"gbifID": anm.id, "datasetKey": anm.datasetKey, "occurrenceID": anm.occur,
                     "kingdom": anm.kingdom, "phylum": anm.phylum, "class": anm.clas, "order": anm.order,
                     "family": anm.fam, "genus": anm.gns,
                     "species": anm.spec, "taxonRank": anm.taxonRank, "scientificName": anm.scientific_name,
                     "verbatimScientificName": anm.verscientific_name,
                     "verbatimScientificNameAuthorship": anm.vscientific_n_auth,
                     "countryCode": anm.countryCode, "locality": anm.locality,
                     "stateProvince": line["stateProvince"], "publishingOrgKey": line["publishingOrgKey"],
                     "decimalLatitude": line["decimalLatitude"], "decimalLongitude": line["decimalLongitude"],
                     "eventDate": line["eventDate"], "day": line["day"], "month": line["month"], "year": line["year"],
                     "taxonKey": line["taxonKey"], "speciesKey": line["speciesKey"], "basisOfRecord": line["basisOfRecord"],
                     "institutionCode": line["institutionCode"],
                     "collectionCode": line["collectionCode"], "catalogNumber": line["catalogNumber"],
                     "dateIdentified": line["dateIdentified"], "license": line["license"], "recordedBy": line["recordedBy"],
                     "lastInterpreted": line["lastInterpreted"], "issue": line["issue"],
                     "sex": line["sex"], "fertility_status": line["fertility_status"], "age": line["age"],
                     "infant(ADDL)": line["infant(ADDL)"], "safety": line["safety"],
                     "special_needs": line["special_needs"]})


    os.remove('edited_gbif.csv')
    os.rename('temp.csv', 'edited_gbif.csv')



