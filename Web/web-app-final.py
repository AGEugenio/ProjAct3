from flask import Flask
from flask import request
from flask import render_template
import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?" 
key = "Ej1k612iGrgYHYUSqvrUyZtkByRg4Ubk"

#Conversion of unit for distance
def convert_distance(dist_unit, unit_length):
    if unit_length.lower()=="mi" or unit_length.lower()=="miles":
        distance = dist_unit
    elif unit_length.lower()=="km" or unit_length.lower()=="kilometer":
        distance =dist_unit * 1.61
    elif unit_length.lower()== "m" or unit_length.lower()=="meter":
        distance = dist_unit * 1610
    return distance

#Conversion of unit for trip duration
def convert_time(t_unit, unit_time):
    if unit_time.lower()== "s" or unit_time.lower()=="seconds":
        time = t_unit
    elif unit_time.lower()== "min" or unit_time.lower()=="minutes":
        time = t_unit / 60
    elif unit_time.lower()== "hr" or unit_time.lower()=="hours":
        time = t_unit / 3600
    return time

#Conversion of unit for fuelused
def convert_vol(v_unit,unit_volume):
    if unit_volume.lower()== "l" or unit_volume.lower()=="liter":
        volume = v_unit *3.785
    elif unit_volume.lower()== "gal" or unit_volume.lower()=="gallon":
        volume = v_unit 
    elif unit_volume.lower()== "bl" or unit_volume.lower()=="barrel":
        volume = v_unit * 0.0317
    return volume

mapquest = Flask(__name__)

@mapquest.route("/")
def main():
    return render_template("form.html")

@mapquest.route('/data', methods=['GET', 'POST'])
def data():
      
    if request.method == 'POST':
        #get the inputs on the answered form
        starting_loc= request.form['starting_loc']
        destination_loc = request.form['destination_loc']
        distance_unit = request.form['distance_unit']
        time_unit = request.form['time_unit']
        volume_unit = request.form['volume_unit']
        route_type = request.form['route_type']
        route_avoid = request.form['route_avoid']
        
        #If the input of locations are empty, an error message would be displayed
        if starting_loc == '' or destination_loc == '':

            return render_template('form.html', error_message = 'Please complete both location fields!',
                                                starting_loc= starting_loc,
                                                destination_loc = destination_loc,
                                                route_type = route_type,
                                                route_avoid = route_avoid)

        #If the given input for other options are empty, an error message would be displayed
        elif distance_unit == '' or time_unit=='' or volume_unit=='' or route_type == '' or route_avoid == '':

            return render_template('form.html', error_message = 'Please complete all the given route options!',
                                                starting_loc = starting_loc,
                                                destination_loc = destination_loc,
                                                route_type = route_type,
                                                route_avoid = route_avoid)

        else:
        
            if route_avoid == "None":
                #the url for api without a route to avoid
                url = main_api + urllib.parse.urlencode({"key": key, 
                                                        "from": starting_loc,
                                                        "routeType": route_type,
                                                        "to": destination_loc}) 
            else:
                #the url for api with a route to avoid
                url = main_api + urllib.parse.urlencode({"key": key, 
                                                        "from": starting_loc,
                                                        "routeType": route_type,
                                                        "to": destination_loc, 
                                                        "avoids": route_avoid}) 
            #get the data from the url
            json_data = requests.get(url).json()
            json_status = json_data["info"]["statuscode"]

            if json_status == 0:
                duration_time=str("{:.2f}".format(convert_time(json_data["route"]["time"], time_unit)))
                duration = json_data["route"]["formattedTime"]
                distance = str("{:.2f}".format(convert_distance(json_data["route"]["distance"], distance_unit)))
                fuel= str("{:.2f}".format(convert_vol(json_data["route"]["fuelUsed"], volume_unit)))

                maneuvers = json_data["route"]["legs"][0]["maneuvers"]
                
                #display output
                return render_template('Info.html', starting_loc = starting_loc, 
                                                    destination_loc = destination_loc,
                                                    time_unit=time_unit,
                                                    duration = duration,
                                                    duration_time=duration_time,
                                                    distance = distance,
                                                    distance_unit = distance_unit,
                                                    fuel = fuel,
                                                    volume_unit=volume_unit,
                                                    route_type = route_type,
                                                    maneuvers = maneuvers)
            else:
                status=str(json_status)
                return render_template('Info.html', error_message = "Status Code: " + status + " Refer to :https://developer.mapquest.com/documentation/directions-api/status-codes",
                                                    starting_loc = starting_loc,
                                                    destination_loc = destination_loc,
                                                    time_unit=time_unit,
                                                    distance_unit = distance_unit,
                                                    volume_unit=volume_unit,
                                                    route_type = route_type)

    return render_template('form.html')
    
if __name__ == "__main__":
    mapquest.run(host="0.0.0.0", port = 5050)