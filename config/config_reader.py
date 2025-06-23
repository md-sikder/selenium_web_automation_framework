# Read environment-specific configurations..

import yaml
import os


def read_config(env='test'):
    with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as file:
        config = yaml.safe_load(file)
    return config['environments'].get(env, config['environments']['test'])
