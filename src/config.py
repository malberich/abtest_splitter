"""Configuration file loader for the experiments configuration."""
import yaml


def load_config():
    """Load the app configuration file."""
    with open('../conf/experiments.yaml', 'r') as config_file:
        try:
            return yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            print(exc)


EXPERIMENTS = load_config()
