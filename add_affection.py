import json
from pathlib import Path
path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
missing_data = [
    ('küssen', 'целовать', {'ich': 'küsse', 'du': 'küsst', 'er/sie/es': 'küsst', 'wir': 'küssen', 'ihr': 'küsst', 'sie/Sie': 'küssen'}, 'Ich küsse meine Mutter.', 'Я целую свою маму.'),
    ('umarmen', 'обнимать', {'ich': 'umarme', 'du': 'umarmst', 'er/sie/es': 'umarmt', 'wir': 'umarmen', 'ihr': 'umarmt', 'sie/Sie': 'umarmen'}, 'Wir umarmen uns freudig.', 'Мы обнимаем друг друга радостно.'),
    ('streicheln', 'гладить', {'ich': 'streichele', 'du': 'streichelst', 'er/sie/es': 'streichelt', 'wir': 'streicheln', 'ihr': 'streichelt', 'sie/Sie': 'streicheln'}, 'Ich streichele die Katze.', 'Я глажу кошку.'),
    ('abholen', 'встречать', {'ich': 'hole ab', 'du': 'holst ab', 'er/sie/es': 'holt ab', 'wir': 'holen ab', 'ihr': 'holt ab', 'sie/Sie': 'holen ab'}, 'Ich hole dich vom Bahnhof ab.', 'Я встречу тебя на вокзале.'),
    ('begleiten', 'провожать', {'ich': 'begleite', 'du': 'begleitest', 'er/sie/es': 'begleitet', 'wir': 'begleiten', 'ihr': 'begleitet', 'sie/Sie': 'begleiten'}, 'Ich begleite dich nach Hause.', 'Я провожу тебя домой.'),
    ('empfangen', 'встречать', {'ich': 'empfange', 'du': 'empfängst', 'er/sie/es': 'empfängt', 'wir': 'empfangen', 'ihr': 'empfangt', 'sie/Sie': 'empfangen'}, 'Wir empfangen unsere Gäste herzlich.', 'Мы встречаем наших гостей сердечно.'),
    ('verabschieden', 'провожать', {'ich': 'verabschiede', 'du': 'verabschiedest', 'er/sie/es': 'verabschiedet', 'wir': 'verabschieden', 'ihr': 'verabschiedet', 'sie/Sie': 'verabschieden'}, 'Ich verabschiede meinen Freund am Flughafen.', 'Я прощаюсь со своим другом в аэропорту.'),
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
