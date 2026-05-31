import json
from pathlib import Path
path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
existing = {v['de'].lower() for v in verbs}
data = [
    ('küssen', 'целовать'),
    ('umarmen', 'обнимать'),
    ('streicheln', 'гладить'),
    ('abholen', 'встречать'),
    ('begleiten', 'провожать'),
    ('empfangen', 'встречать'),
    ('verabschieden', 'провожать'),
]
есть = []
нет = []
for de, ru in data:
    if de.lower() in existing:
        есть.append(f'{de} ({ru})')
    else:
        нет.append(f'{de} ({ru})')
print('ЕСТЬ:', len(есть))
for item in есть:
    print(' ', item)
print('\nНЕТ:', len(нет))
for item in нет:
    print(' ', item)
