import requests
import logging
import re


logging.basicConfig(filename='BusBoard.log', filemode='w', level=logging.DEBUG)  # configures the log


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


class WebApi:
    def __init__(self):
        logging.info("User was asked to enter an AtcoCode.")
        self.atcocode = input("Please enter the code for the bus stop:")
        logging.info("User entered an AtcoCode. The code entered was: " + self.atcocode)
        limit = limit_check()
        self.url = "https://transportapi.com/v3/uk/bus/stop/" + self.atcocode + "///timetable.json?app_id=01b1cb2e&app_key=4dd9957ce60335a0f9c2625ac4041aec&group=no&limit=5=route&limit="+ limit

    def read_url(self):
        r = requests.get(self.url)
        logging.info("Departure information was pulled from the transport API.")
        return r.json()

    def find_departure_details(self, web_dict):
        departure_details = []
        logging.info("Bus departure details are being collected and formatted.")
        resume = True
        while resume:
            try:
                for departure in web_dict["departures"]["all"]:
                    departure_details.append((departure["line_name"], departure["aimed_departure_time"]))
                print("The next buses leaving your stop are:")
                for i in range(0, len(departure_details)):
                    print("Bus number " + departure_details[i][0] + " is leaving at: " + departure_details[i][1])
                logging.info("Bus departure times were displayed to the user.")
                resume = False
            except KeyError:
                print("Sorry. No data was found for the bus stop with AtcoCode: " + self.atcocode)
                logging.info("The user entered an invalid AtcoCode. The user entered: " + self.atcocode)


def main():
    logging.info("Program initialised.")
    print("Welcome to BusBoard.")
    website = WebApi()
    web_response = website.read_url()
    logging.info("Departure information converted into a json format")
    website.find_departure_details(web_response)
    logging.info("Program terminated.")


if __name__ == "__main__": main()
