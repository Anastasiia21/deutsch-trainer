import json
from pathlib import Path

path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
existing = {v['de'].lower() for v in verbs}

# High-frequency daily-life verbs to add one by one.
daily_verbs = [
    'stehen',
    'sitzen',
    'schlafen',
    'öffnen',
    'schließen',
    'warten',
    'bezahlen',
    'helfen',
    'kochen',
    'putzen',
    'laufen',
    'suchen',
    'duschen',
    'ankleiden',
    'einkaufen',
    'vorbereiten',
    'telefonieren',
    'mitnehmen',
    'abwaschen',
    'entspannen'
]

word_data = {
    'stehen': {
        'ru': 'стоять',
        'cases': ['Nominativ'],
        'conjugation': {'ich': 'stehe', 'du': 'stehst', 'er/sie/es': 'steht', 'wir': 'stehen', 'ihr': 'steht', 'sie/Sie': 'stehen'},
        'example_de': 'Ich stehe am Fenster.',
        'example_ru': 'Я стою у окна.'
    },
    'sitzen': {
        'ru': 'сидеть',
        'cases': ['Nominativ'],
        'conjugation': {'ich': 'sitze', 'du': 'sitzt', 'er/sie/es': 'sitzt', 'wir': 'sitzen', 'ihr': 'sitzt', 'sie/Sie': 'sitzen'},
        'example_de': 'Wir sitzen im Wohnzimmer.',
        'example_ru': 'Мы сидим в гостиной.'
    },
    'schlafen': {
        'ru': 'спать',
        'cases': ['Nominativ'],
        'conjugation': {'ich': 'schlafe', 'du': 'schläfst', 'er/sie/es': 'schläft', 'wir': 'schlafen', 'ihr': 'schlaft', 'sie/Sie': 'schlafen'},
        'example_de': 'Er schläft tief.',
        'example_ru': 'Он крепко спит.'
    },
    'öffnen': {
        'ru': 'открывать',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'öffne', 'du': 'öffnest', 'er/sie/es': 'öffnet', 'wir': 'öffnen', 'ihr': 'öffnet', 'sie/Sie': 'öffnen'},
        'example_de': 'Sie öffnet das Fenster.',
        'example_ru': 'Она открывает окно.'
    },
    'schließen': {
        'ru': 'закрывать',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'schließe', 'du': 'schließt', 'er/sie/es': 'schließt', 'wir': 'schließen', 'ihr': 'schließt', 'sie/Sie': 'schließen'},
        'example_de': 'Ich schließe die Tür.',
        'example_ru': 'Я закрываю дверь.'
    },
    'warten': {
        'ru': 'ждать',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'warte', 'du': 'wartest', 'er/sie/es': 'wartet', 'wir': 'warten', 'ihr': 'wartet', 'sie/Sie': 'warten'},
        'example_de': 'Wir warten auf den Bus.',
        'example_ru': 'Мы ждем автобус.'
    },
    'bezahlen': {
        'ru': 'платить',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'bezahle', 'du': 'bezahlst', 'er/sie/es': 'bezahlt', 'wir': 'bezahlen', 'ihr': 'bezahlt', 'sie/Sie': 'bezahlen'},
        'example_de': 'Ich bezahle die Rechnung.',
        'example_ru': 'Я оплачиваю счет.'
    },
    'helfen': {
        'ru': 'помогать',
        'cases': ['Dativ'],
        'conjugation': {'ich': 'helfe', 'du': 'hilfst', 'er/sie/es': 'hilft', 'wir': 'helfen', 'ihr': 'helft', 'sie/Sie': 'helfen'},
        'example_de': 'Er hilft seiner Schwester.',
        'example_ru': 'Он помогает своей сестре.'
    },
    'kochen': {
        'ru': 'готовить',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'koche', 'du': 'kochst', 'er/sie/es': 'kocht', 'wir': 'kochen', 'ihr': 'kocht', 'sie/Sie': 'kochen'},
        'example_de': 'Sie kocht das Abendessen.',
        'example_ru': 'Она готовит ужин.'
    },
    'putzen': {
        'ru': 'убирать',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'putze', 'du': 'putzt', 'er/sie/es': 'putzt', 'wir': 'putzen', 'ihr': 'putzt', 'sie/Sie': 'putzen'},
        'example_de': 'Ich putze das Fenster.',
        'example_ru': 'Я мою окно.'
    },
    'laufen': {
        'ru': 'бежать',
        'cases': ['Nominativ'],
        'conjugation': {'ich': 'laufe', 'du': 'läufst', 'er/sie/es': 'läuft', 'wir': 'laufen', 'ihr': 'lauft', 'sie/Sie': 'laufen'},
        'example_de': 'Wir laufen im Park.',
        'example_ru': 'Мы бегаем в парке.'
    },
    'suchen': {
        'ru': 'искать',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'suche', 'du': 'suchst', 'er/sie/es': 'sucht', 'wir': 'suchen', 'ihr': 'sucht', 'sie/Sie': 'suchen'},
        'example_de': 'Ich suche meine Schlüssel.',
        'example_ru': 'Я ищу свои ключи.'
    },
    'duschen': {
        'ru': 'принимать душ',
        'cases': ['Nominativ'],
        'conjugation': {'ich': 'dusche', 'du': 'duschst', 'er/sie/es': 'duscht', 'wir': 'duschen', 'ihr': 'duscht', 'sie/Sie': 'duschen'},
        'example_de': 'Ich dusche am Morgen.',
        'example_ru': 'Я принимаю душ утром.'
    },
    'ankleiden': {
        'ru': 'одеваться',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'kleide an', 'du': 'kleidest an', 'er/sie/es': 'kleidet an', 'wir': 'kleiden an', 'ihr': 'kleidet an', 'sie/Sie': 'kleiden an'},
        'example_de': 'Ich kleide mein Kind an.',
        'example_ru': 'Я одеваю своего ребенка.'
    },
    'einkaufen': {
        'ru': 'покупать',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'kaufe ein', 'du': 'kaufst ein', 'er/sie/es': 'kauft ein', 'wir': 'kaufen ein', 'ihr': 'kauft ein', 'sie/Sie': 'kaufen ein'},
        'example_de': 'Wir kaufen Lebensmittel ein.',
        'example_ru': 'Мы покупаем продукты.'
    },
    'vorbereiten': {
        'ru': 'готовить',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'bereite vor', 'du': 'bereitest vor', 'er/sie/es': 'bereitet vor', 'wir': 'bereiten vor', 'ihr': 'bereitet vor', 'sie/Sie': 'bereiten vor'},
        'example_de': 'Sie bereitet das Frühstück vor.',
        'example_ru': 'Она готовит завтрак.'
    },
    'telefonieren': {
        'ru': 'звонить',
        'cases': ['Nominativ'],
        'conjugation': {'ich': 'telefoniere', 'du': 'telefonierst', 'er/sie/es': 'telefoniert', 'wir': 'telefonieren', 'ihr': 'telefoniert', 'sie/Sie': 'telefonieren'},
        'example_de': 'Ich telefoniere mit meiner Mutter.',
        'example_ru': 'Я звоню маме.'
    },
    'mitnehmen': {
        'ru': 'взять с собой',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'nehme mit', 'du': 'nimmst mit', 'er/sie/es': 'nimmt mit', 'wir': 'nehmen mit', 'ihr': 'nehmt mit', 'sie/Sie': 'nehmen mit'},
        'example_de': 'Ich nehme meinen Kaffee mit.',
        'example_ru': 'Я беру с собой кофе.'
    },
    'abwaschen': {
        'ru': 'мыть посуду',
        'cases': ['Akkusativ'],
        'conjugation': {'ich': 'wasche ab', 'du': 'wäschst ab', 'er/sie/es': 'wäscht ab', 'wir': 'waschen ab', 'ihr': 'wascht ab', 'sie/Sie': 'waschen ab'},
        'example_de': 'Ich wasche das Geschirr ab.',
        'example_ru': 'Я мою посуду.'
    },
    'entspannen': {
        'ru': 'отдыхать',
        'cases': ['Nominativ'],
        'conjugation': {'ich': 'entspanne', 'du': 'entspannst', 'er/sie/es': 'entspannt', 'wir': 'entspannen', 'ihr': 'entspannt', 'sie/Sie': 'entspannen'},
        'example_de': 'Wir entspannen uns am Abend.',
        'example_ru': 'Мы отдыхаем вечером.'
    }
}

for infinitive in daily_verbs:
    if infinitive not in existing:
        data = word_data[infinitive]
        verbs.append({
            'de': infinitive,
            'ru': data['ru'],
            'cases': data['cases'],
            'conjugation': data['conjugation'],
            'example_de': data['example_de'],
            'example_ru': data['example_ru']
        })
        verbs.sort(key=lambda v: v['de'].lower())
        path.write_text(json.dumps(verbs, ensure_ascii=False, indent=2), encoding='utf8')
        print(f'Added word: {infinitive}')
        break
else:
    print('No new daily word to add.')
