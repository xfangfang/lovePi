import yaml
from var import *

def get_yaml_data(yaml_file):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    return yaml.load(file_data, Loader=yaml.BaseLoader)


if __name__ == '__main__':
    data = get_yaml_data(CONF_START)
    print(data)
