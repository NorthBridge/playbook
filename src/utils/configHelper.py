import re
import json
import logging

logger = logging.getLogger('playbook')

#code from http://stackoverflow.com/questions/18089229/extracting-values-from-deeply-nested-json-structures
def getConfig(key):
    with open('CONFIG', 'r') as jsonConfig:
        data = json.load(jsonConfig)
        for i, p in re.findall(r'(\d+)|(\w+)', key):
            data = data.get(p or int(i), None)
        return data

if __name__ == "__main__":
    print 'token: %s' % getConfig('github.owner')