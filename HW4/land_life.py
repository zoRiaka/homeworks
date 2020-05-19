# This module works with data stored at GBIF web service that was
# collected on animal species in the Biosphere Reserve of W Bénin(Africa)
# data stored in edited_gbif.csv

import csv
import datetime
import timerun
from dateutil import relativedelta

class LandAnimal:
    """This class works only with mentioned earlier dataset.
    Represents general animal class."""

    # Variables that are unchangeable for whole dataset:
    datasetKey = '27f86b34-76dc-485d-a833-b158c6d79bf4'
    kingdom = 'Animalia'
    phylum = 'Chordata'
    clas = 'Mammalia'
    taxonRank = 'SPECIES'
    countryCode = 'BJ'
    locality = 'W Reserve of Biosphere'
    stateProvince = 'Alibori'
    publishingOrgKey = '616e379f-90ed-4c21-9793-8e20f982e9d1'
    basisOfRecord = 'HUMAN_OBSERVATION'
    institutionCode = 'DGEFC'
    licens = 'CC_BY_4_0'
    recordedBy = 'AMAHOWE O. Isidore; CHABI-YAOURE Faï;  GADO Kindo; SINADOUWIROU Theophile'

    # Specified in inherit classes
    order = None
    species_lst = None
    family_lst = None
    speciesKey_lst = None

    def __init__(self, id):
        self.id = str(id) # object will be represented by it's ID as it's the most unique value.

        # Specified in inherit classes
        self._last_check = ""
        self.need_to_be_checked_at = ""
        self._interval = ""
        self._blood_pres_norm = ()
        self._oxygen_level_norm = ()
        self._heartbeat_norm = ()

        # Empty values that are set by user using methods but still are reachable
        self.occur = self.sex = self.spec = self.fam = self.gns = self.age = self.scientific_name = self.verscientific_name = self.vscientific_n_auth = self.eventDate = self.day = self.month = self.year = self.speciesKey = self.collectionCode = self.catalogNumber = self.dateIdentified = self.lastInterpreted = self.issue = self.fertility = self.safety = ""

        self.special_needs = []
        self.latitude = 0.0
        self.longitude = 0.0

    def is_Female(self):
        """True or False if animal is Female or Male"""
        with open("edited_gbif.csv", "r") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter="\t")
            for line in csv_reader:
                if line["gbifID"] == self.id:
                    if line["sex"] == "Female":
                        return True
                    else:
                        return False

    def is_infant(self):
        """True or False if animal is infant"""
        with open("edited_gbif.csv", "r") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter="\t")
            for line in csv_reader:
                if line["gbifID"] == self.id:
                    if line["infant(ADDL)"] == "INFANT":
                        return True
                    else:
                        return False

    def is_dangerous(self):
        """:return: True, false Mildly dangerous"""
        with open("edited_gbif.csv", "r") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter="\t")
            for line in csv_reader:
                if line["gbifID"] == self.id:
                    if line["safety"] == "DANGEROUS":
                        return True
                    elif line["safety"] == "RELATIVELY_DANGEROUS":
                        return "Mildly"
                    else:
                        return False

    def has_needs(self):
        if self.special_needs!=[] and self.special_needs!='[]' and len(self.special_needs)>=1:
            return True
        else:
            return False

    # Next three methods are indicators that check heartbeat, pressure and oxygen level
    # This information does not store anywhere, but if it does go beyond the limit number
    # that is different for all orders of animals, it will signal the user and send a message, this will also
    # open the issue for the animal data


    def check_heartbeat(self):
        if timerun.check_heartbeat(self._heartbeat_norm)!= True:
            self.special_needs.append("HEARTBEAT SENSOR ERROR")


    def check_pressure(self):
        if  timerun.check_pressure(self._blood_pres_norm)!= True:
            self.special_needs.append("BLOOD PRESSURE SENSOR ERROR")

    def check_oxygen_level(self):
        if  timerun.check_pressure(self._blood_pres_norm)!= True:
            self.special_needs.append("OXYGEN LEVEL SENSOR ERROR")

    def get_latitude(self):
        self.latitude = timerun.get_latitude()

    def get_longitude(self):
        self.longitude = timerun.get_longitude()

    def adjust_safety(self):
        pass

    def adjust_spec_needs(self):
        pass


    def main_time(self):
        self.check_pressure()
        self.check_heartbeat()
        self.check_oxygen_level()
        self.get_longitude()
        self.get_latitude()
        self.adjust_safety()
        self.adjust_spec_needs()
        self.need_to_be_checked_at = datetime.date.today() + relativedelta.relativedelta(months=int(self._interval[0]))

    # All methods below are used to set the values by user
    # whilst adding new animal to the dataset
    def set_species(self):
        """"""
        print(f"Species that already are set in this order: {self.species_lst}")
        spec = input("Enter species: ")
        self.spec = spec

    def set_family(self):
        """"""
        print(f"Families that already are set in this order: {self.family_lst}")
        f = input("Enter family: ")
        self.fam = f

    def set_occurance(self):
        occurance = input("Enter occurrenceID: ")
        self.occur = occurance

    def set_gen(self):
        gen = input("Enter genus: ")
        self.gns = gen

    def set_sex(self):
        sx = input("Enter sex: ")
        assert sx in ["Male", "Female"], "Entered value is wrongly formatted."
        self.sex = sx

    def set_age(self):
        age = input("Enter age: ")
        self.age = float(age)

    def set_fertility_status(self):
        fert = input("Enter fertility_status: ")
        self.fertility = fert

    def set_scientificName(self):
        scN = input("Enter scientificName: ")
        self.scientific_name = scN

    def set_verbatimScientificName(self):
        VscN = input("Enter verbatimScientificName: ")
        self.verscientific_name = VscN

    def set_verbatimScientificNameAuthorship(self):
        VscNA = input("Enter verbatimScientificNameAuthorship: ")
        self.vscientific_n_auth = VscNA

    def set_eventDate(self):
        today = datetime.date.today()
        print(f"Is {today}T00:00:00 correct date?")
        dt = input("Enter 'yes' or another eventDate: ")
        if dt == "yes":
            self.eventDate = str(today) + 'T00:00:00'
        else:
            assert dt.endswith('T00:00:00'), "Entered value is wrongly formatted."
            self.eventDate = dt

    def set_day(self):
        dy = datetime.date.today().day
        print(f"Is {dy} correct day?")
        day = input("Enter 'yes' or another day: ")
        if day == "yes":
            self.day = dy
        else:
            assert len(day) > 0 and len(day) < 3, "Entered value is wrongly formatted."
            self.day = day

    def set_month(self):
        mnt = datetime.date.today().month
        print(f"Is {mnt} correct month?")
        month = input("Enter 'yes' or another month: ")
        if month == "yes":
            self.month = month
        else:
            assert len(month) > 0 and len(month) < 3, "Entered value is wrongly formatted."
            self.month = month

    def set_year(self):
        yr = datetime.date.today().year
        print(f"Is {yr} correct year?")
        year = input("Enter 'yes' or another year: ")
        if year == "yes":
            self.year = year
        else:
            assert len(year) == 4, "Entered value is wrongly formatted."
            self.year = year

    def set_speciesKey(self):
        if self.speciesKey_lst == None:
            spKey = input("Enter speciesKey: ")
            assert len(spKey) == 7, "Entered value is wrongly formatted."
            self.speciesKey = spKey
        else:
            for i in self.speciesKey_lst:
                if i[0] == self.spec:
                    self.speciesKey = i[1]

    def set_taxonKey(self):
        if self.speciesKey == '':
            self.taxonKey = 2441039
        else:
            self.taxonKey = self.speciesKey

    def set_collCode(self):
        print(f"Is SSEWPATR_2015 correct collectionCode?")
        collCd = input("Enter 'yes' or another collectionCode: ")
        if collCd == "yes":
            self.collectionCode = "SSEWPATR_2015"
        else:
            self.collectionCode = collCd

    def set_catalNum(self):
        print(f"Is SSEPWATR_2015_430 correct catalogNumber?")
        catalNum = input("Enter 'yes' or another catalogNumber: ")
        if catalNum == "yes":
            self.catalogNumber = "SSEPWATR_2015_430"
        else:
            self.catalogNumber = catalNum

    def set_dtIdent(self):
        print(f"Is 1788-01-01T00:00:00 correct dateIdentified?")
        dtIdent = input("Enter 'yes' or another dateIdentified: ")
        if dtIdent == "yes":
            self.dateIdentified = "1788-01-01T00:00:00"
        else:
            self.dateIdentified = dtIdent

    def set_issue(self):
        print(f"Is GEODETIC_DATUM_ASSUMED_WGS84;COORDINATE_PRECISION_INVALID correct issue?")
        iss = input("Enter 'yes' or another issue: ")
        if iss == "yes":
            self.issue = "GEODETIC_DATUM_ASSUMED_WGS84;COORDINATE_PRECISION_INVALID"
        else:
            self.issue = iss

    def set_lastInterpreted(self):
        tim = str(datetime.datetime.today().time())[:-3]
        dt = str(datetime.datetime.today().date())
        print(f"Is {tim}T{dt}Z correct lastInterpreted time?")
        date = input("Enter 'yes' or another lastInterpreted time: ")
        if date == "yes":
            self.lastInterpreted = tim + 'T' + dt + 'Z'
        else:
            assert date.endswith('Z'), "Entered value is wrongly formatted."
            self.lastInterpreted = date

    # Methods below can be adjust by user as they are changeable and
    # only user can control these variables

    def remove_spec_need(self):
        print(f"Special needs determined for {self.id}: {self.special_needs}")
        need = input("Enter issue that needs to be removed: ")
        self.special_needs.remove(need)

    def change_fertility(self):
        print(f"Current fertility status is: {self.fertility}")
        choice = input("If you want to change it enter 'yes', otherwise enter 'no': ")
        if choice == 'yes':
            fert = input(
                "Choose status from the following: ready_for_fertilization, recently_given_birth, EXPECTANT, INACTIVE: ")
            self.fertility = fert

class Artiodactyla(LandAnimal):
    """Inherited class by animal's order"""
    species_lst = ['Phacochoerus africanus', 'Ourebia ourebi', 'Hippotragus equinus', 'Tragelaphus scriptus',
                   'Kobus ellipsiprymnus', 'Kobus kob', 'Sylvicapra grimmia', 'Syncerus caffer',
                   'Alcelaphus buselaphus', 'Hippopotamus amphibius', '', 'Redunca redunca', 'Potamochoerus porcus']
    family_lst = ['Suidae', 'Bovidae', 'Hippopotamidae']
    speciesKey_lst = [('Ourebia ourebi', '2441135'), ('Hippotragus equinus', '2441030'),
                      ('Tragelaphus scriptus', '5220182'), ('Kobus ellipsiprymnus', '5220160'),
                      ('Kobus kob', '5220161'), ('Sylvicapra grimmia', '2441187'), ('Syncerus caffer', '2441034'),
                      ('Alcelaphus buselaphus', '5220185'), ('Hippopotamus amphibius', '2441247'),
                      ('', ''), ('Redunca redunca', '2441038'), ('Potamochoerus porcus', '2441225')]
    order = "Artiodactyla"

    def __init__(self, id):
        super().__init__(id)
        self.safety = "SAFE"

        self._blood_pres_norm = ('200/100', '280/180')
        self._oxygen_level_norm = ('80', '99')
        self._heartbeat_norm = ('40', '169')


class Primates(LandAnimal):
    """Inherited class by animal's order"""
    species_lst = ['Chlorocebus aethiops', 'Erythrocebus patas', 'Papio anubis']
    family_lst = ['Cercopithecidae']
    speciesKey_lst = [('Chlorocebus aethiops', '2436566'), ('Erythrocebus patas', '2436548'),
                      ('Papio anubis', '5707341')]
    order = "Primates"

    def __init__(self, id):
        super().__init__(id)
        if self.is_infant():
            self.safety = "SAFE"
        elif self.fertility == "recently_given_birth":
            self.safety = "DANGEROUS"
        else:
            self.safety = "RELATIVELY_DANGEROUS"

        self._blood_pres_norm = ('150/100', '200/120')
        self._oxygen_level_norm = ('90', '99')
        self._heartbeat_norm = ('50', '130')


class Carnivora(LandAnimal):
    """Inherited class by animal's order"""
    species_lst = ['Panthera leo', 'Canis adustus', 'Panthera pardus', 'Hyaena hyaena']
    family_lst = ['Felidae', 'Canidae', 'Hyaenidae']
    speciesKey_lst = [('Panthera pardus', '5219436'), ('Hyaena hyaena', '5218777'), ('Panthera leo', '5219404'),
                      ('Canis adustus', '5219146')]
    order = "Carnivora"

    def __init__(self, id):
        super().__init__(id)
        if self.is_infant():
            self.safety = "RELATIVELY_DANGEROUS"
        else:
            self.safety = "DANGEROUS"

        self._blood_pres_norm = ('110/90', '150/60')
        self._oxygen_level_norm = ('75', '99')
        self._heartbeat_norm = ('40', '110')


class Proboscidea(LandAnimal):
    """Inherited class by animal's order"""
    species_lst = ['Loxodonta africana']
    family_lst = ['Elephantidae']
    speciesKey_lst = [('Loxodonta africana', '2435350')]
    order = "Proboscidea"

    def __init__(self, id):
        super().__init__(id)

        self._blood_pres_norm = ('90/60', '140/80')
        self._oxygen_level_norm = ('60', '99')
        self._heartbeat_norm = ('50', '130')




