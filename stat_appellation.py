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
BASIC_FIELDS = ('name', 'type', 'class', 'number')

def is_valid(data) :
    return len(data.get('texts')) > 0

def process_data(data) :
    res = dict()
    for key in ('name',) :
        res[key] = data.get(key)
    try :
        category_text = data.get('category-text')
        category_tags = [s.strip() for s in category_text.split('/')]
        res.update({
            'class' : category_tags[0],
            'number' : category_tags[1] if len(category_tags) == 3 else None,
            'type' : category_tags[-1],
        })
    except :
        print('bad category text:', category_text, file=sys.stderr)
    text = ' '.join(data.get('texts'))
    for key_word in ALL_APPELLATIONS :
        res[key_word] = len(re.findall(key_word, text))
    res['司令'] -= res['司令官']
    appellations = list(sorted(((res[key], key) for key in ALL_APPELLATIONS), reverse=True))
    res['appellation'] = appellations[0][-1] if appellations[0][0] > appellations[1][0] else None
    return res

stats = list()
for line in open(INPUT_FILENAME) :
    data = json.loads(line)
    if is_valid(data) :
        stats.append(process_data(data))
stats.sort(key=lambda x : x['type'])

output_file = open(OUTPUT_FILENAME, 'w') if OUTPUT_FILENAME is not None else sys.stdout
fields = list(BASIC_FIELDS) + list(ALL_APPELLATIONS) + ['appellation']
print(','.join(fields), file=output_file)
for stat in stats :
    print(','.join(str(stat.get(f)) for f in fields), file=output_file)
