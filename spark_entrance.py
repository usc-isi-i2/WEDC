# import sys
# import os

import argparse
from pyspark import SparkContext,SparkConf

import webpage_util
import cleaning_util
import vectorize_util

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


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i','--input_file', required=True)
    arg_parser.add_argument('-s','--seed_file', required=True)
    arg_parser.add_argument('--input_file_format', default='sequence')
    arg_parser.add_argument('--input_data_type', default='json')
    arg_parser.add_argument('--input_separator', default='\t')
    # arg_parser.add_argument('-o','--output_dir', required=True)
    # arg_parser.add_argument('--output_file_format', default='sequence')
    # arg_parser.add_argument('--output_data_type', default='json')
    # arg_parser.add_argument('--output_separator', default='\t')

    args = arg_parser.parse_args()

    # can be inconvenient to specify tab on the command line
    args.input_separator = "\t" if args.input_separator=='tab' else args.input_separator
    # args.output_separator = "\t" if args.output_separator=='tab' else args.output_separator



    sc = SparkContext(appName='WEDC')

    broadcastVar = sc.broadcast([1, 2, 3])

    rdd_jsonlines = webpage_util.load_jsonlines(sc, args.input_file, file_format=args.input_file_format, data_type=args.input_data_type, separator=args.input_separator)

    rdd = rdd_jsonlines.map(webpage_util.map_text).map(cleaning_util.map_clean).map(vectorize_util.map_vectorize)
    

    # print rdd.collect()


"""
spark-submit spark_entrance.py -i /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/webpage_jsonline.jsonl --input_file_format text --input_data_type jsonlines --input_separator '\n'

"""


