import json
from pathlib import Path
file_verbs = {v['de'].lower() for v in json.loads(Path('public/verbs.json').read_text(encoding='utf8'))}
user_list = [
    ('читать', 'lesen'),
    ('смотреть', 'schauen'),
    ('говорить', 'sprechen'),
    ('рассказывать', 'erzählen'),
    ('ссориться', 'sich streiten'),
    ('встречаться', 'sich treffen'),
    ('учиться', 'lernen'),
    ('петь', 'singen'),
    ('танцевать', 'tanzen'),
    ('играть', 'spielen'),
    ('использовать', 'benutzen'),
    ('писать', 'schreiben'),
    ('рисовать', 'zeichnen'),
    ('мыть', 'waschen'),
    ('убирать', 'aufräumen'),
    ('покупать', 'kaufen'),
    ('приносить', 'bringen'),
    ('жить', 'wohnen'),
    ('приезжать', 'ankommen'),
    ('уезжать', 'abfahren'),
    ('летать', 'fliegen'),
    ('мечтать', 'träumen'),
    ('знать', 'wissen'),
    ('думать', 'denken'),
    ('путешествовать', 'reisen'),
]
exists = []
missing = []
for ru, de in user_list:
    if de.lower() in file_verbs:
        exists.append(de)
    else:
        missing.append((ru, de))
print('ЕСТЬ:', len(exists), '→', sorted(exists))
print('НЕТ:', len(missing))
for ru, de in missing:
    print(f'  {de} ({ru})')
