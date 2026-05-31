import json
from pathlib import Path
path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
missing_data = [
    ('schauen', 'смотреть', {'ich': 'schaue', 'du': 'schaust', 'er/sie/es': 'schaut', 'wir': 'schauen', 'ihr': 'schaut', 'sie/Sie': 'schauen'}, 'Ich schaue einen Film.', 'Я смотрю фильм.'),
    ('erzählen', 'рассказывать', {'ich': 'erzähle', 'du': 'erzählst', 'er/sie/es': 'erzählt', 'wir': 'erzählen', 'ihr': 'erzählt', 'sie/Sie': 'erzählen'}, 'Sie erzählt eine Geschichte.', 'Она рассказывает историю.'),
    ('sich streiten', 'ссориться', {'ich': 'streite mich', 'du': 'streitest dich', 'er/sie/es': 'streitet sich', 'wir': 'streiten uns', 'ihr': 'streitet euch', 'sie/Sie': 'streiten sich'}, 'Wir streiten uns nie.', 'Мы никогда не ссоримся.'),
    ('singen', 'петь', {'ich': 'singe', 'du': 'singst', 'er/sie/es': 'singt', 'wir': 'singen', 'ihr': 'singt', 'sie/Sie': 'singen'}, 'Die Kinder singen im Chor.', 'Дети поют в хоре.'),
    ('tanzen', 'танцевать', {'ich': 'tanze', 'du': 'tanzt', 'er/sie/es': 'tanzt', 'wir': 'tanzen', 'ihr': 'tanzt', 'sie/Sie': 'tanzen'}, 'Er tanzt gerne.', 'Ему нравится танцевать.'),
    ('benutzen', 'использовать', {'ich': 'benutze', 'du': 'benutzt', 'er/sie/es': 'benutzt', 'wir': 'benutzen', 'ihr': 'benutzt', 'sie/Sie': 'benutzen'}, 'Ich benutze einen Computer.', 'Я использую компьютер.'),
    ('zeichnen', 'рисовать', {'ich': 'zeichne', 'du': 'zeichnest', 'er/sie/es': 'zeichnet', 'wir': 'zeichnen', 'ihr': 'zeichnet', 'sie/Sie': 'zeichnen'}, 'Das Kind zeichnet Blumen.', 'Ребенок рисует цветы.'),
    ('waschen', 'мыть', {'ich': 'wasche', 'du': 'wäschst', 'er/sie/es': 'wäscht', 'wir': 'waschen', 'ihr': 'wascht', 'sie/Sie': 'waschen'}, 'Sie waschen die Hände.', 'Они моют руки.'),
    ('aufräumen', 'убирать', {'ich': 'räume auf', 'du': 'räumst auf', 'er/sie/es': 'räumt auf', 'wir': 'räumen auf', 'ihr': 'räumt auf', 'sie/Sie': 'räumen auf'}, 'Ich räume mein Zimmer auf.', 'Я убираю свою комнату.'),
    ('bringen', 'приносить', {'ich': 'bringe', 'du': 'bringst', 'er/sie/es': 'bringt', 'wir': 'bringen', 'ihr': 'bringt', 'sie/Sie': 'bringen'}, 'Er bringt mir Blumen.', 'Он мне приносит цветы.'),
    ('ankommen', 'приезжать', {'ich': 'komme an', 'du': 'kommst an', 'er/sie/es': 'kommt an', 'wir': 'kommen an', 'ihr': 'kommt an', 'sie/Sie': 'kommen an'}, 'Wir kommen um 8 Uhr an.', 'Мы приезжаем в 8 часов.'),
    ('abfahren', 'уезжать', {'ich': 'fahre ab', 'du': 'fährst ab', 'er/sie/es': 'fährt ab', 'wir': 'fahren ab', 'ihr': 'fahrt ab', 'sie/Sie': 'fahren ab'}, 'Der Zug fährt um 10 Uhr ab.', 'Поезд уезжает в 10 часов.'),
    ('fliegen', 'летать', {'ich': 'fliege', 'du': 'fliegst', 'er/sie/es': 'fliegt', 'wir': 'fliegen', 'ihr': 'fliegt', 'sie/Sie': 'fliegen'}, 'Der Vogel fliegt hoch.', 'Птица летит высоко.'),
]
existing = {v['de'].lower() for v in verbs}
added = []
for de, ru, conj, ex_de, ex_ru in missing_data:
    if de.lower() not in existing:
        verbs.append({
            'de': de,
            'ru': ru,
            'conjugation': conj,
            'example_de': ex_de,
            'example_ru': ex_ru
        })
        added.append(de)
# Sort
verbs.sort(key=lambda x: x['de'].lower())
path.write_text(json.dumps(verbs, ensure_ascii=False, indent=2), encoding='utf8')
print('added:', added)
print('total verbs:', len(verbs))
