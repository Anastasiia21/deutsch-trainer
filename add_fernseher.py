import json
from pathlib import Path
path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
existing = {v['de'].lower() for v in verbs}
word = {
    'de': 'fernseher',
    'infinitive': 'fernseher',
    'ru': 'телевизор',
    'cases': ['Nominativ', 'Akkusativ'],
    'level': 'A1',
    'conjugation': {},
    'example_de': 'Der Fernseher steht im Wohnzimmer.',
    'example_ru': 'Телевизор стоит в гостиной.'
}
if word['de'].lower() in existing:
    print('already exists:', word['de'])
else:
    verbs.append(word)
    verbs.sort(key=lambda v: v['de'].lower())
    path.write_text(json.dumps(verbs, ensure_ascii=False, indent=2), encoding='utf8')
    print('added:', word['de'])
