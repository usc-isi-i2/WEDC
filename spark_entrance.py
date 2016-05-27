# import sys
# import os

import argparse
from pyspark import SparkContext,SparkConf

import webpage_util

# TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'tests', 'data')
# imd_data_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'imd_san-francisco-maria-2.json'))


# # from wedc.domain.entities.post import Post
# from wedc.domain.core.data.loader import generate_extraction
# from wedc.domain.conf.storage import __res_dir__
# import word2vec

# def loadData(line):
#     import json
#     value = json.loads(line)
#     return [value['sid'], generate_extraction(value['content'])]

APP_NAME = "WEDC"

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i","--input",help = "input file path",required=True)
    arg_parser.add_argument("-o","--output",help = "output file path",required=True)
    arg_parser.add_argument("--file_format",help = "file format text/sequence",default='text')

    args = arg_parser.parse_args()

    sc = SparkContext(appName=APP_NAME)

    webpage_util.generate_jsonlines(sc, args.input, args.output)

    # distFile = sc.textFile(imd_data_, minPartitions=5)
    # parsedData = distFile.map(loadData)
    # print parsedData.collect()

    # sc.stop()