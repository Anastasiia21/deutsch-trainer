import json
from pathlib import Path

path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
existing = {v['de'].lower() for v in verbs}
new_words = [
    {
        'de': 'schicken',
        'infinitive': 'schicken',
        'ru': 'отправлять, посылать',
        'cases': ['Akkusativ', 'Dativ'],
        'level': 'A1',
        'conjugation': {
            'ich': 'schicke',
            'du': 'schickst',
            'er/sie/es': 'schickt',
            'wir': 'schicken',
            'ihr': 'schickt',
            'sie/Sie': 'schicken'
        },
        'example_de': 'Ich schicke dir einen Brief.',
        'example_ru': 'Я отправляю тебе письмо.'
    }
]
added = []
for word in new_words:
    if word['de'].lower() not in existing:
        verbs.append(word)
        added.append(word['de'])

if added:
    verbs.sort(key=lambda v: v['de'].lower())
    path.write_text(json.dumps(verbs, ensure_ascii=False, indent=2), encoding='utf8')

print('added:', added)
print('already existing:', [w['de'] for w in new_words if w['de'].lower() in existing])
