import argparse
import collections
import sys

import requests

parser = argparse.ArgumentParser()
parser.add_argument(
    "-k",
    "--APIKEY",
    help="Google API key. For information on how acquire one refer to: https://developers.google.com/maps/documentation/places/web-service/get-api-key",
    type=str,
)
parser.add_argument(
    "-i",
    "--inputfile",
    help="Input file containing a newline separated list of addresses",
)
parser.add_argument(
    "-o",
    "--outputfile",
    help="Name of output file containing a comma separated list addresses and a given phone number",
)
parser.add_argument(
    "-a", "--address", help="Address to convert to local phone numbers", type=str
)
args = parser.parse_args()


## Error Checking
if len(sys.argv) == 1:
    print(
        "Usage: extract-the-numbers.py [-h/--help] --APIKEY/-k <GOOGLE API KEY> --inputfile/-i <file> --outputfile/-o <outfile> --address/-a <Address to Lookup>"
    )
elif len(sys.argv) != 1:
    if args.APIKEY is None:
        print("Please provide APIKEY via the --APIKEY/-k argument\n")
        quit()
    if args.inputfile or args.address is not None:
        pass
    else:
        print(type(args.address))
        print(type(args.inputfile))
        print("Please provide an address via or -a or an input file via -i\n")
        quit()
    if args.inputfile is not None and args.outputfile is None:
        print("Please provide output file name via the --outputfile/-o argument\n")
        quit()


def get_lat_lng(address):

    lat_lng_params = {"key": args.APIKEY, "query": address, "fields": "lat,lng"}
    lat_lng = requests.get(
        "https://maps.googleapis.com/maps/api/place/textsearch/json?",
        params=lat_lng_params,
    ).json()
    try:
        lat = lat_lng["results"][0]["geometry"]["location"]["lat"]
        lng = lat_lng["results"][0]["geometry"]["location"]["lng"]
        return str(lat) + "," + str(lng)

    except (IndexError, UnboundLocalError):
        print("No lat long found")
        pass


def get_placeIDs(address):
    nearby_params = {
        "key": args.APIKEY,
        "location": get_lat_lng(address),
        "radius": 150,
    }
    nearbyReq = requests.get(
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?",
        params=nearby_params,
    ).json()
    nearby_searches = nearbyReq["results"]
    ## Iterate through JSON and add place_ids to list if not empty
    placeIDList = [i["place_id"] for i in nearby_searches if i["place_id"] is not None]
    return placeIDList


def make_phone_number_list():
    phone_number_list = []
    for i in get_placeIDs(address):
        placeID_params = {
            "key": args.APIKEY,
            "place_id": i,
            "fields": "formatted_phone_number",
        }
        phone_query = requests.get(
            "https://maps.googleapis.com/maps/api/place/details/json?",
            params=placeID_params,
        ).json()
        phone_numbers = phone_query["result"]
        phone_number_list.append(phone_numbers.get("formatted_phone_number"))
    new_list = [i for i in phone_number_list if i]
    phone_number_list = list(
        map(
            lambda x: x.replace("(", "").replace(")", "").replace(" ", ""),
            new_list,  # Remove annoying characters from the list
        )
    )

    return phone_number_list


def landline_or_not(numbers):
    mobiles = ["083", "086", "087", "089", "085"]
    specials = ["180", "008", "081", "185", "189", "076"]
    formatted_numbers = [i[:3] for i in numbers]
    x, y, z = 0, 0, 0
    for i in formatted_numbers:
        if i not in mobiles:
            x += 1
        if i in mobiles:
            y += 1
        if i in specials:
            z += 1
    if x > y:
        return f"landlines are more popular here still {x}:{y}:{z}"
    else:
        return f"mobiles are more popular here {x}:{y}:{z}"


if args.address is not None:
    address = args.address
    print("\nx:y:z\n\nx = lanlines\ny = mobiles\nz = other types")
    print("Lookup Address: " + address + "\n")
    print("List of nearby phone numbers: ")
    print(phone_number_list := make_phone_number_list())
    print(freq := landline_or_not(phone_number_list))

if args.inputfile is not None:
    file = open(args.inputfile, "r")
    Lines = file.readlines()

    ## Setup outfile and headers
    outFile = open(args.outputfile, "a")
    print("\nx:y:z\n\nx = lanlines\ny = mobiles\nz = other types")
    for line in Lines:
        address = line
        print("\n" + "Lookup Address: " + address + "\n")
        print("List of nearby phone numbers: ")
        print(phone_number_list := make_phone_number_list())
        print(freq := landline_or_not(phone_number_list))

        try:
            outFile.writelines((line + "\t" + freq) + "\n")
        except TypeError:
            pass
    outFile.close()
