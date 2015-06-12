import re
import json
import logging

logger = logging.getLogger('playbook')

#code from http://stackoverflow.com/questions/18089229/extracting-values-from-deeply-nested-json-structures
def getConfig(key):
    with open('CONFIG', 'r') as jsonConfig:
        data = json.load(jsonConfig)
        for i, p in re.findall(r'(\d+)|(\w+)', key):
            try:
                data = data[p or int(i)]
            except Exception:
                logger.exception("Unable to retrieve data from CONFIG file" +
                                 " [key=\'%s\'].", key)
                data = None
        return data
