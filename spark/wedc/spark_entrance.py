import sys
import os
import shutil
import argparse
from pyspark import SparkContext, SparkConf, SparkFiles


def load_labelled_data_file(path):
        labelled_data = []
        with open(path, 'rb') as f:
            for line in f.readlines():
                line = line.strip().split('\t')
                labelled_data.append([line[0], line[1]])
        return labelled_data

def load_seed_file(path):
        seeds = {}
        with open(path, 'rb') as f:
            for line in f.readlines():
                line = line.strip().split('\t')
                seeds.setdefault(line[0], line[1])
        return seeds


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i','--input_file', required=True)
    arg_parser.add_argument('-s','--seed_file', required=True)
    arg_parser.add_argument('-l','--labelled_data', required=True)
    arg_parser.add_argument('--lp_jar', required=True)
    arg_parser.add_argument('--enchant_so', required=True)
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

    
    spark_config = SparkConf().setAppName('WEDC')#.setMaster('local[4]')
    # spark_config.setExecutorEnv("PYTHON_EGG_CACHE", System.getenv("/tmp"))
    # spark_config.setExecutorEnv("PYENCHANT_LIBRARY_PATH", libenchant)
    sc = SparkContext(conf=spark_config)
    
    sc.addFile(args.lp_jar)
    # sc.addFile(args.enchant_so)

    # libenchant = SparkFiles.get('libenchant.so.1.6.0')
    # os.environ['PYENCHANT_LIBRARY_PATH'] = libenchant

    import webpage_util
    import cleaning_util
    # import vectorize_util
    # import labelprop_util

    # """
    seeds = load_seed_file(args.seed_file)
    broadcast_seeds = sc.broadcast(seeds)

    labelled_data = load_labelled_data_file(args.labelled_data)
    broadcast_labelled_data = sc.broadcast(labelled_data)

    # implement features first
    # put the code here for broadcast variable only
    from wedc.domain.core.data.seed.seed_vector import generate_vector
    def map_vectorize(data):
        key, tokens = data
        seeds = broadcast_seeds.value
        return (key, generate_vector(tokens, seeds))

    # label prop
    from wedc.domain.core.ml.classifier.label_propagation import labelprop
    def map_labelprop(iterator):
        labelled_data = broadcast_labelled_data.value
        return labelprop.run(list(iterator), labelled_data)

    # reduce
    def reduce_labelprop(a, b):
        # z = x.copy()
        a.update(b)
        return a
    # """
    
    rdd = webpage_util.load_jsonlines(sc, args.input_file, file_format=args.input_file_format, data_type=args.input_data_type, separator=args.input_separator)
    
    rdd = rdd.map(webpage_util.map_text).map(cleaning_util.map_clean)#.map(map_vectorize).mapPartitions(map_labelprop).reduceByKey(reduce_labelprop).groupByKey().mapValues(list)

    # """
    ans = rdd.collect()
    print ans
    # print ans[0][1][0]
    
    # remove output dir
    # if os.path.isdir(args.output_dir):
    #     shutil.rmtree(args.output_dir)
    # rdd.saveAsTextFile(args.output_dir)
    # """


    
""" COMMAND
spark-submit spark_entrance.py -i /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/webpage_jsonline.jsonl --input_file_format text --input_data_type jsonlines --input_separator '\n' -s /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/seeds -l /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelled_data -o /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/spark_output

"""

""" COMMAND
spark-submit --jars /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelprop.jar --driver-class-path /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelprop.jar spark_entrance.py -i /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/webpage_jsonline.jsonl --input_file_format text --input_data_type jsonlines --input_separator '\n' -s /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/seeds -l /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelled_data -o /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/spark_output --lp_jar /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelprop.jar --enchant_so /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/libenchant.so.1.6.0

"""

"""
spark-submit spark_entrance.py -i /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/memex_data --input_file_format sequence --input_data_type json --input_separator '\n' -s /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/seeds -l /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelled_data -o /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/spark_output --lp_jar /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelprop.jar
"""



