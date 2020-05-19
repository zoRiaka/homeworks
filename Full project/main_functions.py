from land_life import Artiodactyla, Proboscidea, Primates, Carnivora
from my_queue import Queue
import datetime
import folium
from dateutil import relativedelta
import geopy.distance
import csv, os

# queues to know when to check animal's sensors
check_one = Queue()  # animals that should be checked every month
check_two = Queue()  # animals that should be checked every second month
check_three = Queue()  # animals that should be checked every third month

animals_lst = []
import csv

with open('edited_gbif.csv', 'r') as f:
    csv_reader = csv.DictReader(f, delimiter="\t")
    for line in csv_reader:
        animal_ord = line["order"]
        if animal_ord == "Artiodactyla":
            anml = Artiodactyla(line["gbifID"])
        elif animal_ord == "Primates":
            anml = Primates(line["gbifID"])
        elif animal_ord == "Carnivora":
            anml = Carnivora(line["gbifID"])
        elif animal_ord == "Proboscidea":
            ml = Proboscidea(line["gbifID"])

        anml.occur = line['occurrenceID']
        anml.fam = line["family"]
        anml.gns = line["genus"]
        anml.specs = line["species"]
        anml.scientific_name = line["scientificName"]
        anml.verscientific_name = line["verbatimScientificName"]
        anml.vscientific_n_auth = line["verbatimScientificNameAuthorship"]
        anml.latitude = line["decimalLatitude"]
        anml.longitude = line["decimalLongitude"]
        anml.eventDate = line["eventDate"]
        anml.day = line["day"]
        anml.month = line["month"]
        anml.year = line["year"]
        anml.set_speciesKey()
        anml.set_taxonKey()
        anml.collectionCode = line["collectionCode"]
        anml.catalogNumber = line["catalogNumber"]
        anml.dateIdentified = line["dateIdentified"]
        anml.recordedBy = line["recordedBy"]
        anml.lastInterpreted = line["lastInterpreted"]
        anml.issue = line["issue"]
        anml.sex = line["sex"]
        anml.fertility = line["fertility_status"]
        anml.age = float(line["age"])
        anml.safety = line["safety"]
        if line["special_needs"]=='[]' or len(line["special_needs"])==0:
            anml.special_needs = list()
        else:
            lst = []
            for i in line["special_needs"].split(","):
                lst.append(i[2:-2])
            anml.special_needs = lst

        animals_lst.append(anml)


def rewrite_queues():
    """Sort animals by three queues depending on time they need to be checked at"""
    for animal in animals_lst:
        if animal.has_needs():
            check_one.enqueue(animal)
            animal._interval = "1 m"
            nextcheck = datetime.date.today() + relativedelta.relativedelta(months=1)
            animal.need_to_be_checked_at = nextcheck
        else:
            if animal.is_infant() or animal.fertility == "EXPECTANT":
                check_two.enqueue(animal)
                animal._interval = "2 m"
                nextcheck = datetime.date.today() + relativedelta.relativedelta(months=2)
                animal.need_to_be_checked_at = nextcheck
            else:
                check_three.enqueue(animal)
                animal._interval = "3 m"
                nextcheck = datetime.date.today() + relativedelta.relativedelta(months=3)
                animal.need_to_be_checked_at = nextcheck



def check():
    """Do the main time check"""
    queues = [check_one, check_two, check_three]
    now_date = datetime.date.today()
    for queue in queues:
        if queue.get_item(0).need_to_be_checked_at == now_date:
            for i in range(queue.size()):
                queue.get_item(i).main_time()
    rewrite_queues()


for i in animals_lst:
    i.last_check = str(datetime.date.today())
rewrite_queues()
for i in animals_lst:
    i.need_to_be_checked_at = datetime.date.today()
check()




def map_gener(coordinates):
    # generate map
    your_coords = (float(coordinates.split(",")[0]), float(coordinates.split(",")[1]))
    m = folium.Map(location=your_coords, zoom_start=15)
    folium.Marker(your_coords, popup="You are here.").add_to(m)
    rad = 3*1000 # radius, 5 kilometers
    folium.Circle(
        radius=rad,
        location=your_coords,
        popup='The Waterfront',
        color='#3186cc',
        fill=True,
    ).add_to(m)

    for i in range(check_one.size()):
        if geopy.distance.vincenty(your_coords, (float(check_one.get_item(i).latitude), float(check_one.get_item(i).longitude))).km <= rad//1000:
            folium.Marker([float(check_one.get_item(i).latitude), float(check_one.get_item(i).longitude)], popup="; ".join(check_one.get_item(i).special_needs), tooltip="First order problems;"+check_one.get_item(i).safety, icon=folium.Icon(color='red', icon="paw")).add_to(m)

    for i in range(check_two.size()):
        if geopy.distance.vincenty(your_coords, (float(check_two.get_item(i).latitude), float(check_two.get_item(i).longitude))).km <= rad//1000:
            folium.Marker([float(check_two.get_item(i).latitude), float(check_two.get_item(i).longitude)], popup="Basic enchanced check", tooltip="Second order problems;"+check_one.get_item(i).safety, icon=folium.Icon(color='green', icon="paw")).add_to(m)

    for i in range(check_three.size()):
        if geopy.distance.vincenty(your_coords, (float(check_three.get_item(i).latitude), float(check_three.get_item(i).longitude))).km <= rad//1000:
            folium.Marker([float(check_three.get_item(i).latitude), float(check_three.get_item(i).longitude)], popup="Basic check", tooltip=check_one.get_item(i).safety, icon=folium.Icon(color='blue', icon="paw")).add_to(m)

    m.save('templates\centralized_map.html')

def overallmap_gener():
    # generate map
    m = folium.Map(location=(11.76387, 2.47058), zoom_start=10)

    for i in range(50):
        folium.Marker([float(check_one.get_item(i).latitude), float(check_one.get_item(i).longitude)], popup="; ".join(check_one.get_item(i).special_needs), tooltip="First order problems;"+check_one.get_item(i).safety, icon=folium.Icon(color='red', icon="paw")).add_to(m)

    for i in range(50):
        folium.Marker([float(check_two.get_item(i).latitude), float(check_two.get_item(i).longitude)], popup="Basic enchanced check", tooltip="Second order problems;"+check_one.get_item(i).safety, icon=folium.Icon(color='green', icon="paw")).add_to(m)

    for i in range(50):
        folium.Marker([float(check_three.get_item(i).latitude), float(check_three.get_item(i).longitude)], popup="Basic check", tooltip="Second order problems;"+check_one.get_item(i).safety, icon=folium.Icon(color='blue', icon="paw")).add_to(m)



    m.save('templates\overall_map.html')

def view_by(view_by, value,headers=None,delimiter="\t"):
    f_n = value+"f.csv"
    with open('edited_gbif.csv', 'r') as f, open(f_n, 'w', newline='') as outf:
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
        for line in csv_reader:
            if line[view_by]==value:
                writer.writerow(
                    {"gbifID": line["gbifID"], "datasetKey": line["datasetKey"], "occurrenceID": line["occurrenceID"],
                     "kingdom": line["kingdom"], "phylum": line["phylum"], "class": line["class"], "order": line["order"],
                     "family": line["family"], "genus": line["genus"],
                     "species": line["species"], "taxonRank": line["taxonRank"], "scientificName": line["scientificName"],
                     "verbatimScientificName": line["verbatimScientificName"],
                     "verbatimScientificNameAuthorship": line["verbatimScientificNameAuthorship"],
                     "countryCode": line["countryCode"], "locality": line["locality"],
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

    with open(f_n) as f:
        content = f.readlines()
    #reading file content into list
    rows = [x.strip() for x in content]
    table = '<table border="1">'
    #creating HTML header row if header is provided
    if headers is not None:
        table+= "".join(["<th>"+cell+"</th>" for cell in headers.split(delimiter)])
    else:
        table+= "".join(["<th>"+cell+"</th>" for cell in rows[0].split(delimiter)])
        rows=rows[1:]
    #Converting csv to html row by row
    for row in rows:
        table+= "<tr>" + "".join(["<td>"+cell+"</td>" for cell in row.split(delimiter)]) + "</tr>" + "\n"
    table+='</table border="1"><br>'
    species_html = open(f"templates/{value}_table.html", "w")
    species_html.write(table)
    os.remove(f_n)
