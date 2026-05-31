import json
from pathlib import Path
path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
existing = {v['de'].lower() for v in verbs}
missing = ['reisen','lernen','denken','kennen','schreiben','hören','träumen','lachen','sich freuen','sich treffen','spielen']
conj = {
    'reisen': {'ich': 'reise','du': 'reist','er/sie/es': 'reist','wir': 'reisen','ihr': 'reist','sie/Sie': 'reisen'},
    'lernen': {'ich': 'lerne','du': 'lernst','er/sie/es': 'lernt','wir': 'lernen','ihr': 'lernt','sie/Sie': 'lernen'},
    'denken': {'ich': 'denke','du': 'denkst','er/sie/es': 'denkt','wir': 'denken','ihr': 'denkt','sie/Sie': 'denken'},
    'kennen': {'ich': 'kenne','du': 'kennst','er/sie/es': 'kennt','wir': 'kennen','ihr': 'kennt','sie/Sie': 'kennen'},
    'schreiben': {'ich': 'schreibe','du': 'schreibst','er/sie/es': 'schreibt','wir': 'schreiben','ihr': 'schreibt','sie/Sie': 'schreiben'},
    'hören': {'ich': 'höre','du': 'hörst','er/sie/es': 'hört','wir': 'hören','ihr': 'hört','sie/Sie': 'hören'},
    'träumen': {'ich': 'träume','du': 'träumst','er/sie/es': 'träumt','wir': 'träumen','ihr': 'träumt','sie/Sie': 'träumen'},
    'lachen': {'ich': 'lache','du': 'lachst','er/sie/es': 'lacht','wir': 'lachen','ihr': 'lacht','sie/Sie': 'lachen'},
    'sich freuen': {'ich': 'freue mich','du': 'freust dich','er/sie/es': 'freut sich','wir': 'freuen uns','ihr': 'freut euch','sie/Sie': 'freuen sich'},
    'sich treffen': {'ich': 'treffe mich','du': 'triffst dich','er/sie/es': 'trifft sich','wir': 'treffen uns','ihr': 'trefft euch','sie/Sie': 'treffen sich'},
    'spielen': {'ich': 'spiele','du': 'spielst','er/sie/es': 'spielt','wir': 'spielen','ihr': 'spielt','sie/Sie': 'spielen'},
}
translations = {
    'reisen': 'путешествовать',
    'lernen': 'учить',
    'denken': 'думать',
    'kennen': 'знать (человека)',
    'schreiben': 'писать',
    'hören': 'слышать',
    'träumen': 'мечтать',
    'lachen': 'смеяться',
    'sich freuen': 'радоваться',
    'sich treffen': 'встречаться',
    'spielen': 'играть'
}
examples = {
    'reisen': ('Wir reisen nach Italien.','Мы путешествуем в Италию.'),
    'lernen': ('Er lernt neue Wörter.','Он учит новые слова.'),
    'denken': ('Ich denke an das Buch.','Я думаю о книге.'),
    'kennen': ('Ich kenne diesen Mann.','Я знаю этого человека.'),
    'schreiben': ('Sie schreibt einen Brief.','Она пишет письмо.'),
    'hören': ('Wir hören das Radio.','Мы слушаем радио.'),
    'träumen': ('Er träumt von Schnee.','Он мечтает о снеге.'),
    'lachen': ('Sie lachen über den Witz.','Они смеются над шуткой.'),
    'sich freuen': ('Ich freue mich auf den Besuch.','Я рад приходу гостей.'),
    'sich treffen': ('Wir treffen uns im Park.','Мы встречаемся в парке.'),
    'spielen': ('Die Kinder spielen draußen.','Дети играют на улице.')
}
added = []
for v in missing:
    if v not in existing:
        verbs.append({
            'de': v,
            'ru': translations[v],
            'conjugation': conj[v],
            'example_de': examples[v][0],
            'example_ru': examples[v][1]
        })
        added.append(v)
path.write_text(json.dumps(verbs, ensure_ascii=False, indent=2), encoding='utf8')
print('added:', added)
