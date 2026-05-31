import json
from pathlib import Path
path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
existing = {v['de'].lower() for v in verbs}
# смеяться → lachen
# шутить → scherzen
# рассказывать → erzählen
# говорить → sprechen
# слышать → hören
# кричать → schreien / rufen
data = [
    ('lachen', 'смеяться'),
    ('scherzen', 'шутить'),
    ('erzählen', 'рассказывать'),
    ('sprechen', 'говорить'),
    ('hören', 'слышать'),
    ('schreien', 'кричать'),
    ('rufen', 'кричать'),
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
