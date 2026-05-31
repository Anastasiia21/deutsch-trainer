import json
from pathlib import Path
file_verbs = {v['de'].lower() for v in json.loads(Path('public/verbs.json').read_text(encoding='utf8'))}
user_list = [
    ('смеяться', 'lachen'),
    ('грустить', 'traurig sein'),
    ('злиться', 'wütend sein'),
    ('радоваться', 'sich freuen'),
    ('быть свободным', 'frei sein'),
    ('быть счастливым', 'glücklich sein'),
    ('быть любимым', 'geliebt werden'),
    ('любить', 'lieben'),
    ('быть сильным', 'stark sein'),
    ('быть слабым', 'schwach sein'),
    ('быть энергичным', 'energiegeladen sein'),
    ('быть подавленным', 'niedergeschlagen sein'),
    ('быть скучным', 'langweilig sein'),
    ('скучать', 'vermissen'),
    ('быть печальным', 'traurig sein'),
    ('печалиться', 'trauern'),
    ('страдать', 'leiden'),
    ('мучиться', 'sich quälen'),
]
exists = []
missing = []
for ru, de_raw in user_list:
    de_list = [x.strip().lower() for x in de_raw.split(',')]
    found = False
    for de in de_list:
        if de in file_verbs:
            exists.append((ru, de))
            found = True
            break
    if not found:
        missing.append((ru, de_raw))
print('ЕСТЬ:', len(exists))
for ru, de in sorted(exists):
    print(f'  {de} ({ru})')
print(f'\nНЕТ: {len(missing)}')
for ru, de in sorted(missing):
    print(f'  {de} ({ru})')
