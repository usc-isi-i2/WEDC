import argparse
from wedc.domain.core.data.loaders import webpages_loader

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i","--input",help = "input file path",required=True)
    arg_parser.add_argument("-o","--output",help = "output file path",required=True)
    args = arg_parser.parse_args()

    webpages_loader.generate_jsonlines(args.input, args.output)

"""
spark-submit jsonlines_helper.py -i /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/webpage_raw -o /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/webpage_jsonline.jsonl

"""