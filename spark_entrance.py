import sys
import os
import shutil
import argparse
from pyspark import SparkContext, SparkConf

from wedc.infrastructure.model.seed_dict import SeedDict

import webpage_util
import cleaning_util
import vectorize_util
import labelprop_util

# TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'tests', 'data')
# imd_data_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'imd_san-francisco-maria-2.json'))


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i','--input_file', required=True)
    arg_parser.add_argument('-s','--seed_file', required=True)
    arg_parser.add_argument('-l','--labelled_data', required=True)
    arg_parser.add_argument('--input_file_format', default='sequence')
    arg_parser.add_argument('--input_data_type', default='json')
    arg_parser.add_argument('--input_separator', default='\t')
    arg_parser.add_argument('-o','--output_dir', required=True)
    # arg_parser.add_argument('--output_file_format', default='sequence')
    # arg_parser.add_argument('--output_data_type', default='json')
    # arg_parser.add_argument('--output_separator', default='\t')

    args = arg_parser.parse_args()

    # can be inconvenient to specify tab on the command line
    args.input_separator = "\t" if args.input_separator=='tab' else args.input_separator
    # args.output_separator = "\t" if args.output_separator=='tab' else args.output_separator

    sc = SparkContext(appName='WEDC')

    seeds = SeedDict.load_seed_file(args.seed_file)
    broadcast_seeds = sc.broadcast(seeds)

    # implement features first
    # put the code here for broadcast variable only
    from wedc.domain.core.data.seed.seed_vector import generate_vector
    def map_vectorize(data):
        key, tokens = data
        seeds = broadcast_seeds.value
        return (key, generate_vector(tokens, seeds))

    from wedc.domain.core.ml.classifier.label_propagation import labelprop
    def map_labelprop(iterator):
        labelled_data = load_labelled_data(args.labelled_data)

        return labelprop.run(list(iterator), labelled_data)

    rdd_jsonlines = webpage_util.load_jsonlines(sc, args.input_file, file_format=args.input_file_format, data_type=args.input_data_type, separator=args.input_separator)

    rdd = rdd_jsonlines.map(webpage_util.map_text).map(cleaning_util.map_clean).map(map_vectorize)#.mapPartitions(labelprop_util.map_labelprop)
    print rdd.collect()
    
    # remove output dir
    if os.path.isdir(args.output_dir):
        shutil.rmtree(args.output_dir)
    rdd.saveAsTextFile(args.output_dir)


    
""" COMMAND
spark-submit spark_entrance.py -i /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/webpage_jsonline.jsonl --input_file_format text --input_data_type jsonlines --input_separator '\n' -s /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/seeds -o /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/spark_output

"""


