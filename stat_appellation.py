import sys
import json
import re

if len(sys.argv) <= 1 :
    sys.exit("Usage: python stat_appellation.py <kanmusu.jsonlines> <output.csv>\n"
        "* Need attr 'texts'. See /kanmusu.jsonliones for example.")
INPUT_FILENAME = sys.argv[1]
OUTPUT_FILENAME = None
if len(sys.argv) > 2 :
    OUTPUT_FILENAME = sys.argv[2]

ALL_APPELLATIONS = ('司令官', '司令', '提督', 'Admiral')

def is_valid(data) :
    return len(data.get('texts')) > 0

def process_data(data) :
    name = data.get('name')
    text = ' '.join(data.get('texts'))
    res = {
        'name' : name,
    }
    for key_word in ALL_APPELLATIONS :
        res[key_word] = len(re.findall(key_word, text))
    res['司令'] -= res['司令官']
    return res

stats = list()
for line in open(INPUT_FILENAME) :
    data = json.loads(line)
    if is_valid(data) :
        stats.append(process_data(data))

output_file = open(OUTPUT_FILENAME, 'w') if OUTPUT_FILENAME is not None else sys.stdout
fields = ['name'] + list(ALL_APPELLATIONS)
print(','.join(fields), file=output_file)
for stat in stats :
    print(','.join(str(stat[f]) for f in fields), file=output_file)
