import json
from pathlib import Path
path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
existing = {v['de'].lower() for v in verbs}
data = [
    'sein', 'haben', 'heißen', 'wohnen', 'leben', 'kommen', 'gehen', 'fahren',
    'reisen', 'arbeiten', 'lernen', 'sprechen', 'verstehen', 'denken', 'wissen',
    'kennen', 'lesen', 'schreiben', 'sehen', 'hören', 'lieben', 'mögen', 'träumen',
    'lachen', 'sich freuen', 'sich treffen', 'kaufen', 'essen', 'trinken', 'spielen'
]
есть = []
нет = []
for de in data:
    if de.lower() in existing:
        есть.append(de)
    else:
        нет.append(de)
print('ЕСТЬ:', len(есть))
for item in есть:
    print(' ', item)
print('\nНЕТ:', len(нет))
for item in нет:
    print(' ', item)
