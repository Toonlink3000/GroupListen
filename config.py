import configparser

class Configurator():
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        try:
            config.read(config_file)
        
