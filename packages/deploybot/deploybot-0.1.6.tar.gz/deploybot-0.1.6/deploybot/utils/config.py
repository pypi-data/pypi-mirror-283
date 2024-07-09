import configparser
from pathlib import Path

CONFIG_FILE = str(Path.home() / '.deploybot_config')

def get_config():
    config = configparser.ConfigParser()
    if not Path(CONFIG_FILE).exists():
        config['DEFAULT'] = {'aws_account_id': '', 'environment': '', 'base_path': '', 'branch': ''}
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(CONFIG_FILE)
    return config

def save_config(aws_account_id, environment, base_path, branch):
    config = get_config()
    config['DEFAULT']['aws_account_id'] = aws_account_id
    config['DEFAULT']['environment'] = environment
    config['DEFAULT']['base_path'] = base_path
    config['DEFAULT']['branch'] = branch
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
