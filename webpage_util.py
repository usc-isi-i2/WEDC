
from pyspark import SparkContext
from digSparkUtil.fileUtil import FileUtil

def load_jsonlines(sc, input, file_format='text', data_type='json'):
    # fUtil = FileUtil(sc)
    # rdd_strings = sc.textFile(input)

    # rdd = fUtil.load_file(input, file_format=file_format, data_type=data_type)
    # print rdd.collect()
    



if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i","--input_file",help = "input file path",required=True)
    arg_parser.add_argument("-o","--output_dir",help = "output dir path",required=True)
    arg_parser.add_argument("--file_format",help = "file format text/sequence",default='text')

    args = arg_parser.parse_args()

    sc = SparkContext(appName='WebPageUtil')

    webpage_util.generate_jsonlines(sc, args.input_file, args.output_dir)