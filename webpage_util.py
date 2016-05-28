import argparse
import re
from pyspark import SparkContext
from digSparkUtil.fileUtil import FileUtil

def load_jsonlines(sc, input, output=None, file_format='text', data_type='jsonlines', separator='\n'):
    fUtil = FileUtil(sc)
    rdd_strings = sc.textFile(input)

    rdd_strings = fUtil.load_file(input, file_format=file_format, data_type=data_type, separator=separator)
    # print rdd_strings.collect()
    return rdd_strings

def load_text(data):
    key, json_obj = data
    text_list = []
    if 'description' in json_obj:
        desc = extract_content(json_obj['description'])
        text_list.append(desc)
    if 'name' in json_obj:
        name = extract_content(json_obj['name'])
        text_list.append(name)
    return (key, ' '.join(text_list))

def extract_content(raw):
    if not raw:
        return ''
    content = []
    if isinstance(raw, basestring):
        content.append(raw)
    else:
        content = raw
    return ' '.join(content)    

# regenerate jsonline for webpages

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i','--input_file', required=True)
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



    sc = SparkContext(appName='WebPageUtil')

    # webpage_util.generate_jsonlines(sc, args.input_file, args.output_dir)
    rdd_jsonlines = load_jsonlines(sc, args.input_file, file_format=args.input_file_format, data_type=args.input_data_type, separator=args.input_separator)

    rdd_text = rdd_jsonlines.map(load_text)
    print rdd_text.collect()


"""
spark-submit webpage_util.py -i /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/webpage_jsonline.jsonl --input_file_format text --input_data_type jsonlines --input_separator '\n'

"""

