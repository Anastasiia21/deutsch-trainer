import json
from pathlib import Path

path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
updated = []
for verb in verbs:
    infinitive = verb.get('de', '')
    new_verb = {
        'de': infinitive,
        'infinitive': infinitive,
        'ru': verb.get('ru', ''),
        'cases': verb.get('cases', []),
        'level': verb.get('level', ''),
        'conjugation': verb.get('conjugation', {}),
        'example_de': verb.get('example_de', ''),
        'example_ru': verb.get('example_ru', ''),
    }
    updated.append(new_verb)
path.write_text(json.dumps(updated, ensure_ascii=False, indent=2), encoding='utf8')
print(f'Added infinitive to {len(updated)} verbs')
