# bulk-number-extractor

```
Be very careful with this
```

## About

A program developed to see if there are any streets with more mobile number operated businesses then the traditional landline operations.
The use of Google's Places API is very important to rip all those numbers out.

## Setup

git clone https://github.com/whatsinmyopsec/bulk-number-extractor
cd into bulk-number-extractor folder

### Install requirements

```
pip install -r requirements.txt
```

## Usage

````
usage: extract-the-numbers.py [-h] [-k APIKEY] [-i INPUTFILE] [-o OUTPUTFILE] [-a ADDRESS]

optional arguments:
  -h, --help            show this help message and exit
  -k APIKEY, --APIKEY APIKEY
                        Google API key. For information on how acquire one refer to:
                        https://developers.google.com/maps/documentation/places/web-
                        service/get-api-key
  -i INPUTFILE, --inputfile INPUTFILE
                        Input file containing a newline separated list of addresses
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        Name of output file containing a comma separated list addresses and a
                        given phone number
  -a ADDRESS, --address ADDRESS
                        Address to convert to local phone numbers```
````

### Example output with a single address:

```
> python extract-the-numbers.py -k <your_api_key> -a "Thomas Street Dublin"

x:y:z

x = landlines
y = mobiles
z = other types
Lookup Address: Thomas Street Dublin

List of nearby phone numbers:
['1800201080', '016364200', '016791709', '0761077180', '014535233', '016798661', '015169106', '016718606', '016991700', '014582336', '014534240', '014735100', '016729488', '016908010', '014893602', '0868923406', '014163558']
landlines are more popular here still 16:1:2
```

### Example output with a list of newline-delimited addresses:

```
> python extract-the-numbers.py -k <your_api_key> -i test.txt -o outx.txt

x:y:z

x = landlines
y = mobiles
z = other types

Lookup Address: Killarney Street Dublin


List of nearby phone numbers:
['018847700', '018363166', '018364935', '018556886', '018847700', '018365677', '018847962', '017645854', '018554363', '015175087', '0851063999', '018881804', '015157241', '018363326', '018764690', '018878404', '018349851', '018178076']
landlines are more popular here still 17:1:0

Lookup Address: Leo Street Dublin

List of nearby phone numbers:
['018032000', '0852085142', '014475195', '0872866598', '018117781', '018306919', '018603426', '0871655673', '0899844897', '016978369', '015674470', '015985831', '0876382415', '0899646929']
landlines are more popular here still 8:6:0
```
