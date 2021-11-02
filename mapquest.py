import urllib.parse
import requests

#API and Key
main_api = "https://www.mapquestapi.com/directions/v2/route?" 
key = "Ej1k612iGrgYHYUSqvrUyZtkByRg4Ubk"

#Conversion of unit
def distance_unit(dist_unit):
    #if unit_length== "mi" or unit_length=="miles" or unit_length=="Miles":
    if unit_length.lower()=="mi" or unit_length.lower()=="miles":
        distance = dist_unit
    elif unit_length.lower()=="km" or unit_length.lower()=="kilometer":
        distance =dist_unit * 1.61
    elif unit_length.lower()== "m" or unit_length.lower()=="meter":
        distance = dist_unit * 1610
    return distance

#The Preferred Unit
def unit_choice(unit_input):  
   #if unit_input== "mi" or unit_input=="miles" or unit_input=="Miles":
   if unit_input=="mi" or unit_input=="miles":
            unit = "mi"
   elif unit_input=="km" or unit_input=="kilometer":
            unit = "km"
   elif unit_input== "m" or unit_input=="meter":
            unit = "m"
   else:
            unit ='0'
   return unit

#The Preferred Route Type  
def route_choose(route_input):
    if route_input in ('fastest','shortest','pedestrian','bicycle'):
        type = route_input
    else:
        type = '0'
    return type
    
while True:
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
  #Choose the preferred unit
    unit_length = input("Select your Preferred Unit |m  km  mi| : ").casefold()
    unit=unit_choice(unit_length)
    if unit == "0":
        print("Invalid Input")
        break
    print("............")
    routeType = input("Select your Preferred Route Type |fastest shortest pedestrian bicycle| : ").casefold()
    type=route_choose(routeType)
    if type == "0": 
        print("Invalid input!")
        break
    print("............")
    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest, "type":type})
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    if json_status == 0:
        distance = distance_unit(json_data["route"]["distance"])
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================")
        print("Directions from " + (orig) + " to " + (dest))
        print("Trip Duration:   " + (json_data["route"]["formattedTime"]))
        print("Distance:      " + str("{:.2f}".format(distance))+ " "+ unit)
        print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78))) 
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
        print("For Staus Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")