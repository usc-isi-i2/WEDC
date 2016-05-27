
from pyspark import SparkContext
from digSparkUtil.fileUtil import FileUtil

def load_jsonlines(sc, input, output=None, file_format='text', data_type='json'):
    fUtil = FileUtil(sc)
    rdd_strings = sc.textFile(input)

    rdd = fUtil.load_file(input, file_format=file_format, data_type=data_type)
    print rdd.collect()
    

# regenerate jsonline for webpages

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_file', required=True)
    parser.add_argument('--input_file_format', default='sequence')
    parser.add_argument('--input_data_type', default='json')
    parser.add_argument('--input_separator', default='\t')
    parser.add_argument('-o','--output_dir', required=True)
    parser.add_argument('--output_file_format', default='sequence')
    parser.add_argument('--output_data_type', default='json')
    parser.add_argument('--output_separator', default='\t')

    args=parser.parse_args()

    # can be inconvenient to specify tab on the command line
    args.input_separator = "\t" if args.input_separator=='tab' else args.input_separator
    args.output_separator = "\t" if args.output_separator=='tab' else args.output_separator


    args = arg_parser.parse_args()

    sc = SparkContext(appName='WebPageUtil')

    webpage_util.generate_jsonlines(sc, args.input_file, args.output_dir)