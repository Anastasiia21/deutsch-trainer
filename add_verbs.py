import json
from pathlib import Path
path = Path('public/verbs.json')
verbs = json.loads(path.read_text(encoding='utf8'))
existing = {v['de'].lower() for v in verbs}
input_text = '''sein	быть
haben	иметь
werden	становиться, стать
gehen	идти
kommen	приходить
machen	делать
sprechen	говорить
wohnen	жить, проживать
arbeiten	работать
lernen	учить, изучать

fahren	ехать
essen	есть
trinken	пить
kaufen	покупать
nehmen	брать
geben	давать
sehen	видеть
finden	находить, считать
wissen	знать (факт)
verstehen	понимать

sein
haben
werden
heißen
kommen
gehen

können
wollen
müssen
sollen
dürfen
mögen

machen
geben
nehmen
sehen
wissen
finden
sprechen
verstehen

essen
trinken
kaufen
fahren
arbeiten
wohnen
lernen
besuchen'''
input_verbs = []
for token in input_text.split():
    if token.strip():
        if '\t' in token:
            german, _ = token.split('\t', 1)
        else:
            german = token
        german = german.strip().lower()
        if german and german not in input_verbs:
            input_verbs.append(german)
# Remove duplicates with existing
verbs_to_add = [v for v in input_verbs if v not in existing]
translations = {
    'sein': 'быть',
    'haben': 'иметь',
    'werden': 'становиться, стать',
    'gehen': 'идти',
    'kommen': 'приходить',
    'machen': 'делать',
    'sprechen': 'говорить',
    'wohnen': 'жить, проживать',
    'arbeiten': 'работать',
    'lernen': 'учить, изучать',
    'fahren': 'ехать',
    'essen': 'есть',
    'trinken': 'пить',
    'kaufen': 'покупать',
    'nehmen': 'брать',
    'geben': 'давать',
    'sehen': 'видеть',
    'finden': 'находить, считать',
    'wissen': 'знать (факт)',
    'verstehen': 'понимать',
    'heißen': 'называться',
    'können': 'мочь, уметь',
    'wollen': 'хотеть',
    'müssen': 'долженствовать',
    'sollen': 'должен',
    'dürfen': 'иметь разрешение',
    'mögen': 'нравиться',
    'besuchen': 'посещать'
}
conjugations = {
    'sein': {'ich':'bin','du':'bist','er/sie/es':'ist','wir':'sind','ihr':'seid','sie/Sie':'sind'},
    'haben': {'ich':'habe','du':'hast','er/sie/es':'hat','wir':'haben','ihr':'habt','sie/Sie':'haben'},
    'werden': {'ich':'werde','du':'wirst','er/sie/es':'wird','wir':'werden','ihr':'werdet','sie/Sie':'werden'},
    'gehen': {'ich':'gehe','du':'gehst','er/sie/es':'geht','wir':'gehen','ihr':'geht','sie/Sie':'gehen'},
    'kommen': {'ich':'komme','du':'kommst','er/sie/es':'kommt','wir':'kommen','ihr':'kommt','sie/Sie':'kommen'},
    'machen': {'ich':'mache','du':'machst','er/sie/es':'macht','wir':'machen','ihr':'macht','sie/Sie':'machen'},
    'sprechen': {'ich':'spreche','du':'sprichst','er/sie/es':'spricht','wir':'sprechen','ihr':'sprecht','sie/Sie':'sprechen'},
    'wohnen': {'ich':'wohne','du':'wohnst','er/sie/es':'wohnt','wir':'wohnen','ihr':'wohnt','sie/Sie':'wohnen'},
    'arbeiten': {'ich':'arbeite','du':'arbeitest','er/sie/es':'arbeitet','wir':'arbeiten','ihr':'arbeitet','sie/Sie':'arbeiten'},
    'lernen': {'ich':'lerne','du':'lernst','er/sie/es':'lernt','wir':'lernen','ihr':'lernt','sie/Sie':'lernen'},
    'fahren': {'ich':'fahre','du':'fährst','er/sie/es':'fährt','wir':'fahren','ihr':'fahrt','sie/Sie':'fahren'},
    'essen': {'ich':'esse','du':'isst','er/sie/es':'isst','wir':'essen','ihr':'esst','sie/Sie':'essen'},
    'trinken': {'ich':'trinke','du':'trinkst','er/sie/es':'trinkt','wir':'trinken','ihr':'trinkt','sie/Sie':'trinken'},
    'kaufen': {'ich':'kaufe','du':'kaufst','er/sie/es':'kauft','wir':'kaufen','ihr':'kauft','sie/Sie':'kaufen'},
    'nehmen': {'ich':'nehme','du':'nimmst','er/sie/es':'nimmt','wir':'nehmen','ihr':'nehmt','sie/Sie':'nehmen'},
    'geben': {'ich':'gebe','du':'gibst','er/sie/es':'gibt','wir':'geben','ihr':'gebt','sie/Sie':'geben'},
    'sehen': {'ich':'sehe','du':'siehst','er/sie/es':'sieht','wir':'sehen','ihr':'seht','sie/Sie':'sehen'},
    'finden': {'ich':'finde','du':'findest','er/sie/es':'findet','wir':'finden','ihr':'findet','sie/Sie':'finden'},
    'wissen': {'ich':'weiß','du':'weißt','er/sie/es':'weiß','wir':'wissen','ihr':'wisst','sie/Sie':'wissen'},
    'verstehen': {'ich':'verstehe','du':'verstehst','er/sie/es':'versteht','wir':'verstehen','ihr':'versteht','sie/Sie':'verstehen'},
    'heißen': {'ich':'heiße','du':'heißt','er/sie/es':'heißt','wir':'heißen','ihr':'heißt','sie/Sie':'heißen'},
    'können': {'ich':'kann','du':'kannst','er/sie/es':'kann','wir':'können','ihr':'könnt','sie/Sie':'können'},
    'wollen': {'ich':'will','du':'willst','er/sie/es':'will','wir':'wollen','ihr':'wollt','sie/Sie':'wollen'},
    'müssen': {'ich':'muss','du':'musst','er/sie/es':'muss','wir':'müssen','ihr':'müsst','sie/Sie':'müssen'},
    'sollen': {'ich':'soll','du':'sollst','er/sie/es':'soll','wir':'sollen','ihr':'sollt','sie/Sie':'sollen'},
    'dürfen': {'ich':'darf','du':'darfst','er/sie/es':'darf','wir':'dürfen','ihr':'dürft','sie/Sie':'dürfen'},
    'mögen': {'ich':'mag','du':'magst','er/sie/es':'mag','wir':'mögen','ihr':'mögt','sie/Sie':'mögen'},
    'besuchen': {'ich':'besuche','du':'besuchst','er/sie/es':'besucht','wir':'besuchen','ihr':'besucht','sie/Sie':'besuchen'}
}
examples = {
    'werden': ('Der Tag wird lang.','День становится длинным.'),
    'machen': ('Ich mache einen Kuchen.','Я делаю пирог.'),
    'sprechen': ('Wir sprechen über den Film.','Мы говорим о фильме.'),
    'wohnen': ('Sie wohnt in einer kleinen Wohnung.','Она живет в небольшой квартире.'),
    'lernen': ('Er lernt die neuen Wörter.','Он учит новые слова.'),
    'kaufen': ('Ich kaufe Brot im Supermarkt.','Я покупаю хлеб в супермаркете.'),
    'nehmen': ('Sie nimmt das Glas.','Она берет стакан.'),
    'geben': ('Er gibt dem Kind ein Buch.','Он дает ребенку книгу.'),
    'sehen': ('Ich sehe den roten Bus.','Я вижу красный автобус.'),
    'finden': ('Wir finden den Schlüssel.','Мы находим ключ.'),
    'wissen': ('Du weißt die Antwort.','Ты знаешь ответ.'),
    'verstehen': ('Sie versteht die Frage.','Она понимает вопрос.'),
    'können': ('Ich kann schon schwimmen.','Я уже могу плавать.'),
    'wollen': ('Wir wollen einen Film sehen.','Мы хотим посмотреть фильм.'),
    'müssen': ('Er muss heute arbeiten.','Он должен сегодня работать.'),
    'sollen': ('Du sollst das Buch lesen.','Ты должен читать книгу.'),
    'dürfen': ('Wir dürfen hier bleiben.','Нам разрешено здесь оставаться.'),
    'mögen': ('Ich mag diese Musik.','Мне нравится эта музыка.'),
    'besuchen': ('Sie besucht ihre Freundin.','Она навещает свою подругу.')
}
added = []
for verb in verbs_to_add:
    if verb not in conjugations:
        raise SystemExit(f'Missing conjugation for {verb}')
    verbs.append({
        'de': verb,
        'ru': translations.get(verb, verb),
        'conjugation': conjugations[verb],
        'example_de': examples[verb][0],
        'example_ru': examples[verb][1]
    })
    added.append(verb)
path.write_text(json.dumps(verbs, ensure_ascii=False, indent=2), encoding='utf8')
print('added', added)
