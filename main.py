import requests
import logging
import re

logging.basicConfig(filename='BusBoard.log', filemode='w', level=logging.DEBUG)  # configures the log


class WebApi:
    def __init__(self):
        logging.info("User was asked to enter an AtcoCode.")
        self.atcocode = input("Please enter the code for the bus stop:")
        logging.info("User entered an AtcoCode. The code entered was: " + self.atcocode)
        limit = limit_check()
        self.url = "https://transportapi.com/v3/uk/bus/stop/" + self.atcocode + "///timetable.json?app_id=01b1cb2e" \
                   "&app_key=4dd9957ce60335a0f9c2625ac4041aec&group=no&limit=" + limit + "nextbuses=no "

    def read_url(self):
        r = requests.get(self.url)  # pulls bus departure information from the transport API about the next bus
        # departures from the chosen stop
        logging.info("Departure information was pulled from the transport API.")
        return r.json()  # converts the information in to a json format

    def find_departure_details(self):
        departure_details = []  # creates a list of departure information to show the user
        logging.info("Bus departure details are being collected and formatted.")
        resume = True
        while resume:
            try:
                self.get_line_and_time(departure_details)
                resume = False
            except KeyError:
                print("Sorry. No data was found for the bus stop with AtcoCode: " + self.atcocode + ". Program "
                                                                                                    "terminated")  # occurs when an invalid AtcoCode is entered by the user
                logging.info("The user entered an invalid AtcoCode. The user entered: " + self.atcocode + ". The"
                                                                                                          "program was terminated.")
                break

    def get_line_and_time(self, lineandtime_dict):  # pulls out information about the bus number and its departure time
        web_response = self.read_url()
        for departure in web_response["departures"]["all"]:
            lineandtime_dict.append((departure["line_name"], departure["aimed_departure_time"]))
        print("The next buses leaving your stop are:")
        for i in range(0, len(lineandtime_dict)):
            print("Bus number " + lineandtime_dict[i][0] + " is leaving at: " + lineandtime_dict[i][1])
        logging.info("Bus departure times were displayed to the user.")


def limit_check():
    cont = True
    while cont:
        limit = input("Please enter how many bus times you would like to see:\n")
        logging.info("User was asked to enter the number of bus times they require.")
        if re.findall(r"\d+", limit):
            logging.info("The user chose to see " + limit + " bus time(s).")
            return limit
        else:
            print("Sorry. That value is invalid.")
            logging.info("The user entered an invalid limit value. The value they entered was: " + limit + ".")


def main():
    logging.info("Program initialised.")
    print("Welcome to BusBoard.")
    website = WebApi()
    logging.info("Departure information converted into a json format")
    website.find_departure_details()
    logging.info("Program terminated.")


if __name__ == "__main__": main()
