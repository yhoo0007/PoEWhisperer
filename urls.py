import json
from re import match


DEFAULT_CONFIG_FP = 'config.json'


def validate_url(url):
    return match('https://www.pathofexile.com/trade/search/\w*/(\w*)', url) is not None


def add_url(config_fp=DEFAULT_CONFIG_FP):
    with open(config_fp) as config_file:
        config = json.load(config_file)
    
    print('\nAdd search urls to config file. Ctrl + C to terminate')
    while True:
        try:
            url, label = input('Enter (url;label): ').split(';')
            if validate_url(url):
                if url not in config['urls'].values():
                    config['urls'][label] = url
                    print('Url added\n')
                else:
                    print('Url already exists')
            else:
                print('Invalid url provided\n')
        except KeyboardInterrupt:
            terminate = input('\nTerminate? (Y/N)')
            if terminate in ('Y', 'y'):
                with open(config_file, 'w') as config_file:
                    json.dump(config, config_file, indent=4)
                print('Changes saved')
                return 0


def remove_url(config_fp=DEFAULT_CONFIG_FP):
    with open(config_fp) as config_file:
        config = json.load(config_file)

    print('\nRemove search urls from config file. Ctrl + C to terminate')
    while True:
        for label, url in config['urls'].items():
            print(label, url)
        input_ = input('Enter label or url to remove: ')
        try:
            config['urls'].pop(input_)
            print('Url removed')
        except KeyError:
            num_removed = 0
            for k, v in config['urls'].items():
                if v == input_:
                    config['urls'].pop(k)
                    num_removed += 1
            print(f'{num_removed} url(s) removed')
        except KeyboardInterrupt:
            terminate = input('\nTerminate? (Y/N)')
            if terminate in ('Y', 'y'):
                with open(config_fp, 'w') as config_file:
                    json.dump(config, config_file, indent=4)
                print('Changes saved')
                return 0
