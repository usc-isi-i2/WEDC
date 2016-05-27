import argparse
import json
import os
import re

from wedc.domain.core.data import loader
 
WEBPAGE_SOURCE = '_source'  # list
WEBPAGE_NAME = 'name'   # list
WEBPAGE_URI = 'uri' # string 
WEBPAGE_DESC = 'description'    # string


def generate_jsonlines(input, output):
    import jsonlines

    pn_file = open(input, 'rU')
    raw = json.load(pn_file)
    pn_file.close()
    hits = raw['hits']['hits']

    obj = jsonlines.open(output, mode='w')
    for hit in hits:
        source = hit[WEBPAGE_SOURCE]
        obj.dump(source)

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i","--input",help = "input file path",required=True)
    arg_parser.add_argument("-o","--output",help = "output file path",required=True)
    args = arg_parser.parse_args()

    generate_jsonlines(input, output)

