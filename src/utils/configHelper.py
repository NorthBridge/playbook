import os
import re
import json

#code from http://stackoverflow.com/questions/18089229/extracting-values-from-deeply-nested-json-structures
def getConfig(key):
    configFile = os.path.join(os.path.dirname(__file__), 'CONFIG')
    with open(configFile, 'r') as jsonConfig:
        data = json.load(jsonConfig)
        for i, p in re.findall(r'(\d+)|(\w+)', key):
            try:
                data = data[p or int(i)]
            except Exception:
                #TODO: Log error
                data = None
        return data
