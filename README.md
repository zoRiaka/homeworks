# Animal tracking with GBIF database
http://gbifgetinfo.pythonanywhere.com/

The main goal of the project was to design a simple web page that will process data taken from a random GBIF's dataset and based on the user's commands either display a map (either centralized and eddited recording to the coordinates written by user or map of all reserve territory) or, display data accordingly to the user's choice. The main idea and functionalities are imitations of sensors that check heartbeat, blood pressure ect. Their update takes place accordingly to the categories that depend on problems and special needs of an animal.

# Basic functional

When go to the website, the first choice you will need to do depends on either you want to view a map or get more detailed information on animals. Next:
1. If you chose map:
You than will have to choose to either view general or centralized map.
If you choose general, you will get a map featuring animals, marked with different markers. Markers depend on whether animal have special care needed or are under more concentrated watch. If the case is first one, animal will be marked with red marker. The second option will give you animals marked with green, and if the needs required by animal are basic, the mark will be blue. The icons will display additional information such as if the animal is dangerous and in some cases problems or state they have. Basically, the marking follows by the principle that the animals are being checked on with different time interval. One being a reserve worker may also consider checking and updationg info on animals starting with red markers.
If your choise is centralized map, you need to write down your coordinates.
**Please note that coordinates should be written as a float values and split by coma as it is in example**.
Once you've done that, the displayed map will have all criterias mentioned above, only this time animals will be displayed only within a **three kilometres radius** with your point as a center.
2. If you want to view information:
The three choices you will be given are all based on the same principal. You either have to write down id, speices or key that specifies the species. The written values have to meet the requirments. In order to do that **follow instructions written above submit button**. Once you've submited your request, a table will be displayed with either one speices or a single animal with given id.


# Libraries and modules

In order to localy run module from console, you will need to install next modules:
flask, folium, csv, pandas, os
