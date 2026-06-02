import json
from pathlib import Path

path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
existing = {v['de'].lower() for v in verbs}
new_words = [
    {
        'de': 'schlafen',
        'infinitive': 'schlafen',
        'ru': 'спать',
        'cases': ['Nominativ'],
        'level': 'A1',
        'conjugation': {
            'ich': 'schlafe',
            'du': 'schläfst',
            'er/sie/es': 'schläft',
            'wir': 'schlafen',
            'ihr': 'schlaft',
            'sie/Sie': 'schlafen'
        },
        'example_de': 'Ich schlafe am Wochenende lange.',
        'example_ru': 'Я сплю долго на выходных.'
    },
    {
        'de': 'ausschlafen',
        'infinitive': 'ausschlafen',
        'ru': 'высыпаться',
        'cases': ['Nominativ'],
        'level': 'A2',
        'conjugation': {
            'ich': 'schlafe aus',
            'du': 'schläfst aus',
            'er/sie/es': 'schläft aus',
            'wir': 'schlafen aus',
            'ihr': 'schlaft aus',
            'sie/Sie': 'schlafen aus'
        },
        'example_de': 'Am Sonntag kann ich ausschlafen.',
        'example_ru': 'В воскресенье я могу выспаться.'
    },
    {
        'de': 'treffen',
        'infinitive': 'treffen',
        'ru': 'встречать, встречаться',
        'cases': ['Akkusativ'],
        'level': 'A1',
        'conjugation': {
            'ich': 'treffe',
            'du': 'triffst',
            'er/sie/es': 'trifft',
            'wir': 'treffen',
            'ihr': 'trefft',
            'sie/Sie': 'treffen'
        },
        'example_de': 'Wir treffen uns um acht.',
        'example_ru': 'Мы встречаемся в восемь.'
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
print('requested existing:', [word['de'] for word in new_words if word['de'].lower() in existing])
