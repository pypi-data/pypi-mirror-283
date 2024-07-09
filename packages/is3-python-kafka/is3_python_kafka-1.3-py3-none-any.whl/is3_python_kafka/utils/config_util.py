import configparser
import os


def get_header(filePath, key):
    # 上传的文件路径
    key_config = load_config(filePath)[key]
    headers = {
        'Content-Type': 'application/json',
        'X-Access-Key': key_config.get('X-Access-Key'),
        'X-Secret-Key': key_config.get('X-Secret-Key')
    }
    return headers


def get_server_name(filePath, key):
    key_config = load_config(filePath)[key]
    serverName = key_config.get('server-name')
    return serverName


def get_property(filePath, key, property):
    key_config = load_config(filePath)[key]
    value = key_config.get(property)
    return value


def load_config(configPath):
    config_path = os.path.join(configPath)

    # 确认文件存在
    if os.path.exists(config_path):
        print(f"Config file exists at: {config_path}")
    else:
        print(f"Config file does not exist at: {config_path}")
        exit(1)

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_path)

    return config
