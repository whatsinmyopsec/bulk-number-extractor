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
        params=lat_long_params,
    )
    try:
        lat = lat_lng.json()["results"][0]["geometry"]["location"]["lat"]
        lng = lat_lng.json()["results"][0]["geometry"]["location"]["lng"]
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
    )
    nearby_searches = nearbyReq.json()["results"]
    placeIDList = []

    ## Iterate through JSON and add place_ids to list if not empty
    for i in nearby_searches:
        if i["place_id"] is not None:
            placeIDList.append(i["place_id"])

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
        )
        phone_numbers = phone_query.json()["result"]
        phone_number_list.append(phone_numbers.get("formatted_phone_number"))

    for x in phone_number_list:
        if x == None:  # Remove bugged None from the list
            phone_number_list.remove(x)
    phone_number_list = list(
        map(
            lambda x: x.replace("(", "").replace(")", "").replace(" ", ""),
            phone_number_list,
        )
    )
    # Remove annoying characters from the list

    return phone_number_list


def most_common(numbers):
    prefix_l = 3

    prefix_counter = collections.Counter()
    for i in numbers:
        prefix = i[:prefix_l]
        prefix_counter[prefix] += 1

    for prefix, number_of_similarities in prefix_counter.most_common():
        return f"{number_of_similarities} numbers started with `{prefix}`"


if args.address is not None:
    address = args.address
    print("Lookup Address: " + address + "\n")
    print("List of nearby phone numbers: ")
    print(phone_number_list := make_phone_number_list())
    print("\nMost common prefix: ")
    print(most_common(phone_number_list))

if args.inputfile is not None:
    file = open(args.inputfile, "r")
    Lines = file.readlines()

    ## Setup outfile and headers
    outFile = open(args.outputfile, "a")

    for line in Lines:
        address = line
        print("Lookup Address: " + address + "\n")

        print("List of nearby phone numbers: ")
        print(phone_number_list := make_phone_number_list())
        print("\nMost common prefix: ")
        print(similar_number := most_common(phone_number_list))

        try:
            outFile.writelines((line + "\t" + similar_number) + "\n")
        except TypeError:
            pass
    outFile.close()