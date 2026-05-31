import json
from pathlib import Path
path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
missing_data = [
    ('scherzen', 'шутить', {'ich': 'scherze', 'du': 'scherzst', 'er/sie/es': 'scherzt', 'wir': 'scherzen', 'ihr': 'scherzt', 'sie/Sie': 'scherzen'}, 'Ich scherze mit meinen Freunden.', 'Я шучу с моими друзьями.'),
    ('schreien', 'кричать', {'ich': 'schreie', 'du': 'schreist', 'er/sie/es': 'schreit', 'wir': 'schreien', 'ihr': 'schreit', 'sie/Sie': 'schreien'}, 'Das Baby schreit laut.', 'Малыш громко кричит.'),
    ('rufen', 'кричать', {'ich': 'rufe', 'du': 'rufst', 'er/sie/es': 'ruft', 'wir': 'rufen', 'ihr': 'ruft', 'sie/Sie': 'rufen'}, 'Ich rufe nach Hilfe.', 'Я кричу о помощи.'),
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
