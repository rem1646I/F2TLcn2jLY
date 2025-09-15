# 代码生成时间: 2025-09-15 11:43:23
# config_manager.py
# A Bottle-based application for managing configuration files.

from bottle import route, run, request, response
import json
import os

# Define the path to store configuration files
CONFIG_DIR = './configs/'

# Create the configuration directory if it doesn't exist
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

class ConfigManager:
    """Class to manage configuration files."""
    def __init__(self):
        pass

    def load_config(self, filename):
        """Load configuration from a file."""
        try:
            with open(os.path.join(CONFIG_DIR, filename), 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None

    def save_config(self, filename, config):
        """Save configuration to a file."""
        try:
            with open(os.path.join(CONFIG_DIR, filename), 'w') as file:
                json.dump(config, file)
        except Exception as e:
            raise e

    def delete_config(self, filename):
        """Delete a configuration file."""
        try:
            os.remove(os.path.join(CONFIG_DIR, filename))
        except FileNotFoundError:
            pass
        except Exception as e:
            raise e

# Create an instance of ConfigManager
config_manager = ConfigManager()

# Define the Bottle routes
@route('/config/<filename>', method='GET')
def get_config(filename):
    """Return the configuration for a given filename."""
    config = config_manager.load_config(filename)
    if config is None:
        response.status = 404
        return {'error': 'Configuration not found'}
    return config

@route('/config/<filename>', method='PUT')
def update_config(filename):
    """Update or create a configuration file."""
    if request.json is None:
        response.status = 400
        return {'error': 'Invalid JSON payload'}
    try:
        config = request.json
        config_manager.save_config(filename, config)
        return {'message': 'Configuration updated successfully'}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

@route('/config/<filename>', method='DELETE')
def delete_config_route(filename):
    """Delete a configuration file."""
    try:
        config_manager.delete_config(filename)
        return {'message': 'Configuration deleted successfully'}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# Run the Bottle application
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)