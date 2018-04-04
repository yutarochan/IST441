import json

fnmap = json.loads(open('../../../data/oer_commons_dump/fn_map.json', 'r').read())
for i in fnmap:
    print i
