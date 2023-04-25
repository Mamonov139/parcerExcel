import configparser
import os

configs = configparser.ConfigParser()


# basePath = r'C:\Users\mamonov\Documents\domeo-erp\Config'
# basePath = r'C:\Users\travovalex\estimate\domeo-erp\Config'
basePath = os.path.dirname(os.path.abspath(__file__))
configs.read(fr"{basePath}\overlay.ini", encoding='utf-8')