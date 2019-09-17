import requests
import logging
import re
from flask import request

logging.basicConfig(filename='BusBoard.log', filemode='w', level=logging.DEBUG)  # configures the log


class Departure:
    def __init__(self, time, destination, line_num):
        self.time = time
        self.destination = destination
        self.line_num = line_num


class Stop:
    def __init__(self, name, departures):
        self.name = name
        self.departures = departures


class PostcodeApi:
    def __init__(self, postcode, stops):
        self.postcode = postcode
        self.stops = stops

    def postcode_check(self):
        if re.search(r"(\D{1,2}\w{1,2}? ?\d\D+)", self.postcode.lower()):
            postcode_url = "https://api.postcodes.io/postcodes/" + self.postcode.lower()
            return postcode_url
        else:
            logging.info("User entered an invalid postcode. The postcode entered was: " + self.postcode.lower())
            print("Sorry. That postcode was not recognised. Program terminated.")

    def read_postcode_url(self):
        pc_url = self.postcode_check()
        read = requests.get(pc_url)
        logging.info("Postcode's information was pulled from the postcode API.")
        return read.json()

    def get_lat_long(self):
        web_pc_response = self.read_postcode_url()
        logging.info("Latitude and longitude were retrieved for the requested postcode")
        return web_pc_response["result"]["latitude"], web_pc_response["result"]["longitude"]


class TransportApi:
    def __init__(self, postcode):
        latitude, longitude = postcode.get_lat_long()
        i_d, key = get_secrets()  # gets my API key and ID from a separate document not stored on GitHub
        self.url = "https://transportapi.com/v3/uk/places.json?app_id=" + i_d[0] + "&app_key=" + key[0] + "&lat=" \
                   + str(latitude) + "&lon=" + str(longitude) + "&type=bus_stop"

    def read_url(self):
        r = requests.get(self.url)  # pulls bus departure information from the transport API about the next bus
        # departures from the chosen stop
        logging.info("Departure information was pulled from the transport API.")
        return r.json()  # converts the information in to a json format

    def get_nearest_stops(self, bus_stops):  # pulls out information about the bus number and its departure time
        web_response = self.read_url()
        for bus_stop in web_response["member"]:
            bus_stops.append(bus_stop["atcocode"])
        stop1 = bus_stops[0]
        stop2 = bus_stops[1]
        return stop1, stop2

    def find_bus_departures(self):
        limit = limit_check()
        i_d, key = get_secrets()
        nearest_stops = []
        stop1, stop2 = self.get_nearest_stops(nearest_stops)
        url_stop1 = "https://transportapi.com/v3/uk/bus/stop/" + stop1 + "///timetable.json?app_id=" + i_d[0] + \
                    "&app_key=" + key[0] + "&group=no&limit=" + limit + "nextbuses=no "
        url_stop2 = "https://transportapi.com/v3/uk/bus/stop/" + stop2 + "///timetable.json?app_id=" + i_d[0] + \
                    "&app_key=" + key[0] + "&group=no&limit=" + limit + "nextbuses=no "

        return url_stop1, url_stop2

    def read_bus_dep_url(self):
        url_stop1, url_stop2 = self.find_bus_departures()
        read_stop1 = requests.get(url_stop1)
        read_stop2 = requests.get(url_stop2)

        stop1_json = read_stop1.json()
        stop2_json = read_stop2.json()

        return stop1_json, stop2_json


def get_secrets():  # function that reads my private API ID and key from a secret text file
    with open("secrets.txt", "r") as file:
        secret_contents = file.read()
        i_d = re.findall(r"App ID: (\w{8})", secret_contents)
        key = re.findall(r"Key: (\w{32})", secret_contents)
        logging.info("API Key and ID retrieved successfully.")
    return i_d, key


def limit_check():
    cont = True
    while cont:
        limit = request.args.get("limit")
        logging.info("User was asked to enter the number of bus times they require.")
        if re.findall(r"\d+", limit):
            logging.info("The user chose to see " + limit + " bus time(s).")
            return limit
        else:
            print("Sorry. That value is invalid.")
            logging.info("The user entered an invalid limit value. The value they entered was: " + limit + ".")
