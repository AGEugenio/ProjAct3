#import libraries
import urllib.parse
import requests
import os 

#API and Key
main_api = "https://www.mapquestapi.com/directions/v2/route?" 
key = "Ej1k612iGrgYHYUSqvrUyZtkByRg4Ubk"

#Conversion of unit for distance
def distance_unit(dist_unit):
    if unit_length.lower()=="mi" or unit_length.lower()=="miles":
        distance = dist_unit
    elif unit_length.lower()=="km" or unit_length.lower()=="kilometer":
        distance =dist_unit * 1.61
    elif unit_length.lower()== "m" or unit_length.lower()=="meter":
        distance = dist_unit * 1610
    return distance

#Conversion of unit for trip duration
def time_unit(t_unit):
    if unit_time.lower()== "s" or unit_time.lower()=="seconds":
        time = t_unit
    elif unit_time.lower()== "min" or unit_time.lower()=="minutes":
        time = t_unit / 60
    elif unit_time.lower()== "hr" or unit_time.lower()=="hours":
        time = t_unit / 3600
    return time

#Conversion of unit for fuelused
def vol_unit(v_unit):
    if unit_volume.lower()== "l" or unit_volume.lower()=="liter":
        volume = v_unit *3.785
    elif unit_volume.lower()== "gal" or unit_volume.lower()=="gallon":
        volume = v_unit 
    elif unit_volume.lower()== "bl" or unit_volume.lower()=="barrel":
        volume = v_unit * 0.0317
    return volume


#The Preferred Unit of Distance
def unit_choice(unit_input):  
   if unit_input=="mi" or unit_input=="miles":
        unit = "mi"
   elif unit_input=="km" or unit_input=="kilometer":
        unit = "km"
   elif unit_input== "m" or unit_input=="meter":
        unit = "m"
   else:
        unit ='0'
   return unit

#The Preferred unit of time for Trip Duration
def time_choice(time_input):
    if unit_time== "s" or unit_time=="seconds" :
        time_input = "s"

    elif unit_time=="min" or unit_time=="minutes":
        time_input = "min"
            
    elif unit_time== "hr" or unit_time=="hours" :
        time_input = "hr"

    else:
        time_input='0'
    return time_input

#The Preferred Unit of Volume for Usage of Fuel
def vol_choice(vol_input):
    if unit_volume== "l" or unit_volume=="liter" :
        vol_input = "l"

    elif unit_volume == "gal" or unit_volume=="gallon":
        vol_input = "gal" 
    elif unit_volume== "bl" or unit_volume=="barrel":
        vol_input = "bl"
    else:
        vol_input='0'
    return vol_input

#The Preferred Route Type  
def route_choose(route_input):
    if route_input in ('fastest','shortest','pedestrian','bicycle'):
        type = route_input
    else:
        type = '0'
    return type

#The Preferred Route to Avoid
def avoid_choice(avoid_input):
    if avoid_input in ('limited access highway' , 'toll road', 'ferry' , 'unpaved' , 'approximate seasonal closure' , 'country border crossing' , 'bridge' , 'tunnel', 'none'):
       avoid = avoid_input 
    else:
        avoid = '0'
    return avoid
    
while True:
    #Getting the Location
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break

    #Choose the preferred unit of distance
    unit_length = input("Select your Preferred Unit |m  km  mi| : ").casefold()
    unit=unit_choice(unit_length)
    if unit == "0":
        print("Invalid Input")
        break
    print("............")
    
    #Choose the preffered unit of time
    unit_time = input("Select your Preferred Unit | s  min  hr |: ").casefold()
    unit_t=time_choice(unit_time)
    if unit_t == "0":
        print("Invalid Input")
        break
    print("............")

    #Choose the preffered unit of volume
    unit_volume= input("Select your Preferred Unit | gal  l  bl |: ").casefold()
    unit_v=vol_choice(unit_volume)
    if unit_v == "0":
        print("Invalid Input")
        break
    print("............")

    #Choose the preferred route type
    routeType = input("Select your Preferred Route Type |fastest shortest pedestrian bicycle| : ").casefold()
    type=route_choose(routeType)
    if type == "0": 
        print("Invalid input!")
        break
    print("............")

    #Choose the route to avoid
    routeAvoid = input ("Select the route you want to avoid? [ Limited Access Highway | Toll Road | Ferry | Unpaved | Approximate Seasonal Closure | Country Border Crossing | Bridge | Tunnel | None ]: ").casefold()
    avoid = avoid_choice(routeAvoid)
    if avoid == "0":
        print("Invalid input!")
        break
    elif avoid == "none":
        #Calling the API that only has no route to avoid
        url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest, "routeType":type})
    else:
        #Calling the API that has route to avoid
        url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest, "routeType":type, "avoids":avoid})
    
    #Clear screen
    os.system("clear")

    #Print and get data from URL
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    #Display of Output
    if json_status == 0:
        time = time_unit(json_data["route"]["time"])
        distance = distance_unit(json_data["route"]["distance"])
        volume = vol_unit(json_data["route"]["fuelUsed"])

        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================")
        print("Directions from " + (orig) + " to " + (dest))
        print("Trip Duration:   " + str("{:.2f}".format(time) + " " + unit_t + " | " +(json_data["route"]["formattedTime"])))
        print("Distance:      " + str("{:.2f}".format(distance))+ " "+ unit)
        print("Fuel Used: " + str("{:.2f}".format(volume))+ " " + unit_v) 
        print("=============================================")
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            distance = distance_unit(each["distance"])
            print((each["narrative"]) + " (" + str("{:.2f}".format(distance)) + " " + unit + ")")
        print("=============================================\n")
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
    else:
        print("************************************************************************")
        print("For Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")