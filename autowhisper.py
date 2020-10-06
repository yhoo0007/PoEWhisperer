import sys, getopt
import live_search
import filters
import urls
import json


LIVE_SEARCH_ARGS = ['livesearch', 'ls']
ADD_FILTER_ARGS = ['addfilter', 'af']
REMOVE_FILTER_ARGS = ['removefilter', 'rf']
ADD_URL_ARGS = ['addurl', 'au']
REMOVE_URL_ARGS = ['removeurl', 'ru']

DEFAULT_CONFIG_FP = 'config.json'


def print_help():
    print('Usage: python autowhisper.py <operand> <arg>')
    print('Valid operands are: -o -h')
    print(f'Valid args are: {LIVE_SEARCH_ARGS + ADD_FILTER_ARGS + REMOVE_FILTER_ARGS + ADD_URL_ARGS + REMOVE_URL_ARGS}')


def get_config(config_fp=DEFAULT_CONFIG_FP):
    with open(config_fp) as config_file:
        return json.load(config_file)


if __name__ == '__main__':
    try:
        ops, _ = getopt.getopt(sys.argv[1:], "ho:",)
        ops, = ops
    except Exception:
        print_help()
        sys.exit(2)
    
    op, arg = ops
    exit_code = 0
    if op == '-h':
        print_help()
        exit_code = 2
    elif op == '-o':
        config = get_config()
        if arg in LIVE_SEARCH_ARGS:
            live_search.main(config['urls'], config['league'])
        elif arg in ADD_FILTER_ARGS:
            filters.add_filter()
        elif arg in REMOVE_FILTER_ARGS:
            filters.remove_filter()
        elif arg in ADD_URL_ARGS:
            urls.add_url()
        elif arg in REMOVE_URL_ARGS:
            urls.remove_url()
        else:
            print('Invalid arg provided')
            print_help()
            exit_code = 2
    else:
        print('Invalid operand provided.')
        print_help()
        exit_code = 2
    
    sys.exit(exit_code)