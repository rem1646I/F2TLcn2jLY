# 代码生成时间: 2025-09-11 16:22:04
from bottle import Bottle, run, request, response
import json
import os

# 定义配置文件管理器
class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}
        except json.JSONDecodeError:
            self.config = {}

    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def save_config(self, config):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            raise IOError("Failed to save config: " + str(e))

    def update_config(self, key, value):
        if key in self.config:
            self.config[key] = value
        else:
            raise KeyError(f"Key '{key}' not found in config")
        self.save_config(self.config)

    def get_config(self, key):
        return self.config.get(key, None)

# 创建一个Bottle应用
app = Bottle()

# 配置文件路径
CONFIG_PATH = 'config.json'
config_manager = ConfigManager(CONFIG_PATH)

@app.route('/config/<key>', method='GET')
def get_config(key):
    try:
        value = config_manager.get_config(key)
        if value is None:
            response.status = 404
            return {'error': 'Config key not found'}
        return {'value': value}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

@app.route('/config/<key>', method='PUT')
def update_config(key):
    try:
        if not request.json:
            response.status = 400
            return {'error': 'No JSON provided'}

        value = request.json.get('value')
        if value is None:
            response.status = 400
            return {'error': 'No value provided'}

        config_manager.update_config(key, value)
        return {'message': 'Config updated successfully'}
    except KeyError as e:
        response.status = 404
        return {'error': str(e)}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

if __name__ == '__main__':
    run(app, host='localhost', port=8080)