import argparse
from filter import filter_based_pandas, filter_based_hashlib


def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('--input_path', type=str, help='Input file path')
    parser.add_argument('--output_path', type=str, help='Output file path')
    parser.add_argument('--key_list', deafult="", action='store_true', help='Increase output verbosity')
    parser.add_argument('--dataformat', deafult="alpaca", type=str, help='dataformat')
    parser.add_argument('--strategy', deafult="pandas", type=str, help='Input file path')
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    key_list = args.key_list

    if args.strategy == "pandas":
        filter_based_pandas(input_path=input_path,
                            output_path=output_path,
                            key_list=key_list)
        
    elif args.strategy == "hashlib":
        filter_based_hashlib(input_path=input_path,
                            output_path=output_path)
    



