import yaml
import os

def load_config(config_path='config.yaml'):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

_config = load_config()

# Data paths
DATA_DIR = _config['data']['dir']
SYMBOLS_CSV = os.path.join(DATA_DIR, _config['data']['symbols_file'])
STOCK_PRICES_CSV = _config['data']['stock_prices_file']
METRICS_CSV = _config['data']['metrics_file']

# Fetch settings
LOOKBACK_DAYS = _config['fetch']['lookback_days']

# Metrics settings
WINDOW_SHORT = _config['metrics']['window_short']
WINDOW_LONG = _config['metrics']['window_long']
PREDICT_DAYS = _config['metrics']['predict_days']
