import json
from pathlib import Path
path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
existing = {v['de'].lower() for v in verbs}
word = {
    'de': 'fernsehen',
    'infinitive': 'fernsehen',
    'ru': 'смотреть телевизор',
    'cases': ['Akkusativ'],
    'level': 'A1',
    'conjugation': {
        'ich': 'sehe fern',
        'du': 'siehst fern',
        'er/sie/es': 'sieht fern',
        'wir': 'sehen fern',
        'ihr': 'seht fern',
        'sie/Sie': 'sehen fern'
    },
    'example_de': 'Ich sehe abends gern fern.',
    'example_ru': 'Я люблю смотреть телевизор по вечерам.'
}
if word['de'].lower() in existing:
    print('already exists:', word['de'])
else:
    verbs.append(word)
    verbs.sort(key=lambda v: v['de'].lower())
    path.write_text(json.dumps(verbs, ensure_ascii=False, indent=2), encoding='utf8')
    print('added:', word['de'])
