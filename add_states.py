import json
from pathlib import Path
path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
missing_data = [
    ('geliebt werden', 'быть любимым', {'ich': 'werde geliebt', 'du': 'wirst geliebt', 'er/sie/es': 'wird geliebt', 'wir': 'werden geliebt', 'ihr': 'werdet geliebt', 'sie/Sie': 'werden geliebt'}, 'Ich werde von meiner Familie geliebt.', 'Я любим своей семьей.'),
    ('traurig sein', 'грустить', {'ich': 'bin traurig', 'du': 'bist traurig', 'er/sie/es': 'ist traurig', 'wir': 'sind traurig', 'ihr': 'seid traurig', 'sie/Sie': 'sind traurig'}, 'Er ist heute traurig.', 'Он сегодня грустит.'),
    ('niedergeschlagen sein', 'быть подавленным', {'ich': 'bin niedergeschlagen', 'du': 'bist niedergeschlagen', 'er/sie/es': 'ist niedergeschlagen', 'wir': 'sind niedergeschlagen', 'ihr': 'seid niedergeschlagen', 'sie/Sie': 'sind niedergeschlagen'}, 'Sie ist niedergeschlagen.', 'Она подавлена.'),
    ('frei sein', 'быть свободным', {'ich': 'bin frei', 'du': 'bist frei', 'er/sie/es': 'ist frei', 'wir': 'sind frei', 'ihr': 'seid frei', 'sie/Sie': 'sind frei'}, 'Ich bin endlich frei.', 'Я наконец свободен.'),
    ('stark sein', 'быть сильным', {'ich': 'bin stark', 'du': 'bist stark', 'er/sie/es': 'ist stark', 'wir': 'sind stark', 'ihr': 'seid stark', 'sie/Sie': 'sind stark'}, 'Er ist sehr stark.', 'Он очень сильный.'),
    ('langweilig sein', 'быть скучным', {'ich': 'bin langweilig', 'du': 'bist langweilig', 'er/sie/es': 'ist langweilig', 'wir': 'sind langweilig', 'ihr': 'seid langweilig', 'sie/Sie': 'sind langweilig'}, 'Das Film ist langweilig.', 'Фильм скучный.'),
    ('schwach sein', 'быть слабым', {'ich': 'bin schwach', 'du': 'bist schwach', 'er/sie/es': 'ist schwach', 'wir': 'sind schwach', 'ihr': 'seid schwach', 'sie/Sie': 'sind schwach'}, 'Ich bin schwach nach der Krankheit.', 'Я слаб после болезни.'),
    ('glücklich sein', 'быть счастливым', {'ich': 'bin glücklich', 'du': 'bist glücklich', 'er/sie/es': 'ist glücklich', 'wir': 'sind glücklich', 'ihr': 'seid glücklich', 'sie/Sie': 'sind glücklich'}, 'Wir sind sehr glücklich.', 'Мы очень счастливы.'),
    ('energiegeladen sein', 'быть энергичным', {'ich': 'bin energiegeladen', 'du': 'bist energiegeladen', 'er/sie/es': 'ist energiegeladen', 'wir': 'sind energiegeladen', 'ihr': 'seid energiegeladen', 'sie/Sie': 'sind energiegeladen'}, 'Die Kinder sind energiegeladen.', 'Дети энергичны.'),
    ('wütend sein', 'злиться', {'ich': 'bin wütend', 'du': 'bist wütend', 'er/sie/es': 'ist wütend', 'wir': 'sind wütend', 'ihr': 'seid wütend', 'sie/Sie': 'sind wütend'}, 'Er ist wütend auf mich.', 'Он злится на меня.'),
    ('sich quälen', 'мучиться', {'ich': 'quäle mich', 'du': 'quälst dich', 'er/sie/es': 'quält sich', 'wir': 'quälen uns', 'ihr': 'quält euch', 'sie/Sie': 'quälen sich'}, 'Ich quäle mich mit Gedanken.', 'Я мучусь мыслями.'),
    ('trauern', 'печалиться', {'ich': 'traure', 'du': 'trauerst', 'er/sie/es': 'trauert', 'wir': 'trauern', 'ihr': 'trauert', 'sie/Sie': 'trauern'}, 'Sie trauert um ihren Freund.', 'Она печалится о своем друге.'),
    ('vermissen', 'скучать', {'ich': 'vermisse', 'du': 'vermisst', 'er/sie/es': 'vermisst', 'wir': 'vermissen', 'ihr': 'vermisst', 'sie/Sie': 'vermissen'}, 'Ich vermisse dich sehr.', 'Я по тебе очень скучаю.'),
    ('leiden', 'страдать', {'ich': 'leide', 'du': 'leidest', 'er/sie/es': 'leidet', 'wir': 'leiden', 'ihr': 'leidet', 'sie/Sie': 'leiden'}, 'Er leidet unter Kopfschmerzen.', 'Он страдает от головной боли.'),
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
