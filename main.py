import requests
import logging


class WebApi:
    def __init__(self):
        self.atcocode = input("Please enter the code for the bus stop:")
        logging.info("User entered an AtcoCode. The code entered was: " + self.atcocode)
        self.limit = int(input("Please enter how many bus times you would like to see:"))
        logging.info("The user chose to see " + self.limit + " bus time(s).")
        self.url = "https://transportapi.com/v3/uk/bus/stop/" + self.atcocode + "///timetable.json?app_id=01b1cb2e&app_key=4dd9957ce60335a0f9c2625ac4041aec&group=no&limit=5=route&limit="+ self.limit

    def read_url(self):
        r = requests.get(self.url)
        return r.json()
    


def find_departure_details(web_dict):
    departure_details = []
    for departure in web_dict["departures"]["all"]:
        departure_details.append((departure["line_name"], departure["aimed_departure_time"]))
    print("The next buses leaving your stop are:")
    for i in range(0, len(departure_details)):
        print("Bus number " + departure_details[i][0] + " is leaving at: " + departure_details[i][1])


def main():
    logging.info("Program initialised.")
    print("Welcome to BusBoard.")
    website = WebApi()
    web_data = website.read_url()
    find_departure_details(web_data)


if __name__ == "__main__": main()
