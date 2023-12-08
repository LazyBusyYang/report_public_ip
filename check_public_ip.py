import argparse
import requests
import sys


def main(args) -> int:
    with open(args.input_path, 'r') as f_read:
        last_ip = f_read.read().strip()
    this_ip = requests.get('https://api.ipify.org').content.decode('utf8')
    if this_ip == last_ip:
        ret_val = 0
        msg = 'Current IP equals to last IP.'
    else:
        ret_val = 1
        msg = f'Current IP {this_ip} is different from last IP {last_ip}.'
    if args.output_path is not None:
        with open(args.output_path, 'w') as f_write:
            f_write.write(this_ip)
    print(msg)
    return ret_val


def setup_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--input_path',
        help='Path to a file saving public ip got last time.',
        type=str,
        required=True)
    parser.add_argument(
        '--output_path',
        help='Path to a file saving public ip got this time.',
        type=str,
        required=False)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = setup_parser()
    ret_val = main(args)
    sys.exit(ret_val)
