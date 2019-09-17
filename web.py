from flask import Flask, render_template, request
import logging
from postcode import PostcodeApi, TransportApi, Stop, Departure

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/busInfo")
def busInfo():
    postcode = request.args.get('postcode')
    stops = []
    logging.info("Program initialised.")
    postcode_info = PostcodeApi(postcode, stops)
    transport_info = TransportApi(postcode_info)
    postcode_info.get_lat_long()
    logging.info("Program complete.")

    get_departure_details = PostcodeApi(postcode, [])
    first_stop, second_stop = transport_info.read_bus_dep_url()
    for raw_stop in [first_stop]:
        stop = Stop(raw_stop["name"], [])
        for raw_dep in raw_stop["departures"]["all"]:
            dep = Departure(raw_dep["aimed_departure_time"], raw_dep["direction"], raw_dep["line_name"])
            stop.departures.append(dep)
        get_departure_details.stops.append(stop)
    for raw_stop in [second_stop]:
        stop = Stop(raw_stop["name"], [])
        for raw_dep in raw_stop["departures"]["all"]:
            dep = Departure(raw_dep["aimed_departure_time"], raw_dep["direction"], raw_dep["line_name"])
            stop.departures.append(dep)
        get_departure_details.stops.append(stop)
    logging.info("Program terminated.")
    return render_template('info.html', postcode=postcode, stops=get_departure_details.stops)


if __name__ == "__main__": app.run()
