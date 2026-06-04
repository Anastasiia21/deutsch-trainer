import json
from pathlib import Path

NEW_VERBS_PATH = Path('new_verbs.txt')
PUBLIC_VERBS_PATH = Path('public/verbs.json')

SEPARATORS = [' - ', ' — ', ':', '\t']
CONJUGATION_KEYS = ['ich', 'du', 'er/sie/es', 'wir', 'ihr', 'sie/Sie']
MAX_IMPORTS_PER_RUN = 1


def regular_conjugation(stem, infinitive):
    return {
        'ich': f'{stem}e',
        'du': f'{stem}st',
        'er/sie/es': f'{stem}t',
        'wir': infinitive,
        'ihr': f'{stem}t',
        'sie/Sie': infinitive,
    }


def entry(de, ru, cases, level, conjugation, example_de, example_ru, infinitive=None):
    return {
        'de': de,
        'infinitive': infinitive or de,
        'ru': ru,
        'cases': cases,
        'level': level,
        'conjugation': conjugation,
        'example_de': example_de,
        'example_ru': example_ru,
    }


# Curated queue data. The importer must never invent placeholder cards: a verb is
# imported only when all fields below are present and pass validation.
VERB_DATA = {
    'wehtun': entry(
        'wehtun', 'болеть / причинять боль', ['Dativ'], 'A1',
        {'ich': 'tue weh', 'du': 'tust weh', 'er/sie/es': 'tut weh', 'wir': 'tun weh', 'ihr': 'tut weh', 'sie/Sie': 'tun weh'},
        'Mir tut der Kopf weh.', 'У меня болит голова.'
    ),
    'schmerzen': entry(
        'schmerzen', 'болеть / причинять боль', ['Nominativ'], 'A2', regular_conjugation('schmerz', 'schmerzen'),
        'Mein Rücken schmerzt.', 'У меня болит спина.'
    ),
    'verurteilen': entry(
        'verurteilen', 'осуждать / приговаривать', ['Akkusativ'], 'B1', regular_conjugation('verurteil', 'verurteilen'),
        'Ich verurteile Gewalt.', 'Я осуждаю насилие.'
    ),
    'erklären': entry(
        'erklären', 'объяснять', ['Dativ', 'Akkusativ'], 'A2', regular_conjugation('erklär', 'erklären'),
        'Kannst du mir das erklären?', 'Ты можешь мне это объяснить?'
    ),
    'befehlen': entry(
        'befehlen', 'приказывать', ['Dativ'], 'B1',
        {'ich': 'befehle', 'du': 'befiehlst', 'er/sie/es': 'befiehlt', 'wir': 'befehlen', 'ihr': 'befehlt', 'sie/Sie': 'befehlen'},
        'Der Chef befiehlt es nicht.', 'Начальник этого не приказывает.'
    ),
    'aushalten': entry(
        'aushalten', 'выдерживать / терпеть', ['Akkusativ'], 'B1',
        {'ich': 'halte aus', 'du': 'hältst aus', 'er/sie/es': 'hält aus', 'wir': 'halten aus', 'ihr': 'haltet aus', 'sie/Sie': 'halten aus'},
        'Ich halte den Lärm nicht aus.', 'Я не выдерживаю этот шум.'
    ),
    'schützen': entry(
        'schützen', 'защищать', ['Akkusativ'], 'A2', regular_conjugation('schütz', 'schützen'),
        'Eine Jacke schützt mich vor Kälte.', 'Куртка защищает меня от холода.'
    ),
    'träumen': entry(
        'träumen', 'мечтать / видеть сон', ['Dativ'], 'A2', regular_conjugation('träum', 'träumen'),
        'Ich träume von Urlaub.', 'Я мечтаю об отпуске.'
    ),
    'backen': entry(
        'backen', 'печь / выпекать', ['Akkusativ'], 'A2',
        {'ich': 'backe', 'du': 'backst', 'er/sie/es': 'backt', 'wir': 'backen', 'ihr': 'backt', 'sie/Sie': 'backen'},
        'Ich backe einen Kuchen.', 'Я пеку пирог.'
    ),
    'bedürfen': entry(
        'bedürfen', 'нуждаться / требовать', ['Genitiv'], 'B2',
        {'ich': 'bedarf', 'du': 'bedarfst', 'er/sie/es': 'bedarf', 'wir': 'bedürfen', 'ihr': 'bedürft', 'sie/Sie': 'bedürfen'},
        'Das bedarf keiner Erklärung.', 'Это не требует объяснения.'
    ),
    'beginnen': entry(
        'beginnen', 'начинать / начинаться', ['Akkusativ'], 'A1',
        {'ich': 'beginne', 'du': 'beginnst', 'er/sie/es': 'beginnt', 'wir': 'beginnen', 'ihr': 'beginnt', 'sie/Sie': 'beginnen'},
        'Der Kurs beginnt heute.', 'Курс начинается сегодня.'
    ),
    'bergen': entry(
        'bergen', 'спасать / таить в себе', ['Akkusativ'], 'B2',
        {'ich': 'berge', 'du': 'birgst', 'er/sie/es': 'birgt', 'wir': 'bergen', 'ihr': 'bergt', 'sie/Sie': 'bergen'},
        'Die Situation birgt ein Risiko.', 'Ситуация таит в себе риск.'
    ),
    'betrügen': entry(
        'betrügen', 'обманывать', ['Akkusativ'], 'B1',
        {'ich': 'betrüge', 'du': 'betrügst', 'er/sie/es': 'betrügt', 'wir': 'betrügen', 'ihr': 'betrügt', 'sie/Sie': 'betrügen'},
        'Er betrügt seine Freundin nicht.', 'Он не обманывает свою девушку.'
    ),
    'beweisen': entry(
        'beweisen', 'доказывать', ['Dativ', 'Akkusativ'], 'B1',
        {'ich': 'beweise', 'du': 'beweist', 'er/sie/es': 'beweist', 'wir': 'beweisen', 'ihr': 'beweist', 'sie/Sie': 'beweisen'},
        'Ich beweise dir das.', 'Я докажу тебе это.'
    ),
    'bewerben': entry(
        'sich bewerben', 'подавать заявление / откликаться на вакансию', ['Akkusativ'], 'B1',
        {'ich': 'bewerbe mich', 'du': 'bewirbst dich', 'er/sie/es': 'bewirbt sich', 'wir': 'bewerben uns', 'ihr': 'bewerbt euch', 'sie/Sie': 'bewerben sich'},
        'Ich bewerbe mich um eine Stelle.', 'Я откликаюсь на вакансию.', infinitive='sich bewerben'
    ),
    'biegen': entry(
        'biegen', 'сгибать / поворачивать', ['Akkusativ'], 'B1',
        {'ich': 'biege', 'du': 'biegst', 'er/sie/es': 'biegt', 'wir': 'biegen', 'ihr': 'biegt', 'sie/Sie': 'biegen'},
        'Bieg links ab.', 'Поверни налево.'
    ),
    'binden': entry(
        'binden', 'завязывать / связывать', ['Akkusativ'], 'B1',
        {'ich': 'binde', 'du': 'bindest', 'er/sie/es': 'bindet', 'wir': 'binden', 'ihr': 'bindet', 'sie/Sie': 'binden'},
        'Ich binde meine Schuhe.', 'Я завязываю обувь.'
    ),
    'bieten': entry(
        'bieten', 'предлагать', ['Dativ', 'Akkusativ'], 'B1',
        {'ich': 'biete', 'du': 'bietest', 'er/sie/es': 'bietet', 'wir': 'bieten', 'ihr': 'bietet', 'sie/Sie': 'bieten'},
        'Das Hotel bietet Frühstück an.', 'Отель предлагает завтрак.'
    ),
    'bitten': entry(
        'bitten', 'просить', ['Akkusativ'], 'A2',
        {'ich': 'bitte', 'du': 'bittest', 'er/sie/es': 'bittet', 'wir': 'bitten', 'ihr': 'bittet', 'sie/Sie': 'bitten'},
        'Ich bitte dich um Hilfe.', 'Я прошу тебя о помощи.'
    ),
    'bleiben': entry(
        'bleiben', 'оставаться', ['Nominativ'], 'A1',
        {'ich': 'bleibe', 'du': 'bleibst', 'er/sie/es': 'bleibt', 'wir': 'bleiben', 'ihr': 'bleibt', 'sie/Sie': 'bleiben'},
        'Ich bleibe heute zu Hause.', 'Сегодня я остаюсь дома.'
    ),
    'brechen': entry(
        'brechen', 'ломать / нарушать', ['Akkusativ'], 'B1',
        {'ich': 'breche', 'du': 'brichst', 'er/sie/es': 'bricht', 'wir': 'brechen', 'ihr': 'brecht', 'sie/Sie': 'brechen'},
        'Er bricht die Regel.', 'Он нарушает правило.'
    ),
    'brennen': entry(
        'brennen', 'гореть / жечь', ['Nominativ'], 'A2',
        {'ich': 'brenne', 'du': 'brennst', 'er/sie/es': 'brennt', 'wir': 'brennen', 'ihr': 'brennt', 'sie/Sie': 'brennen'},
        'Das Licht brennt noch.', 'Свет ещё горит.'
    ),
    'dürfen': entry(
        'dürfen', 'мочь / иметь разрешение', ['Nominativ'], 'A1',
        {'ich': 'darf', 'du': 'darfst', 'er/sie/es': 'darf', 'wir': 'dürfen', 'ihr': 'dürft', 'sie/Sie': 'dürfen'},
        'Darf ich kurz fragen?', 'Можно я быстро спрошу?'
    ),
    'empfehlen': entry(
        'empfehlen', 'рекомендовать', ['Dativ', 'Akkusativ'], 'A2',
        {'ich': 'empfehle', 'du': 'empfiehlst', 'er/sie/es': 'empfiehlt', 'wir': 'empfehlen', 'ihr': 'empfehlt', 'sie/Sie': 'empfehlen'},
        'Ich empfehle dir diesen Film.', 'Я рекомендую тебе этот фильм.'
    ),
}


def parse_line(line):
    raw = line.strip()
    if not raw or raw.startswith('#'):
        return None
    for sep in SEPARATORS:
        if sep in raw:
            parts = [p.strip() for p in raw.split(sep, 1)]
            if len(parts) == 2 and parts[0]:
                return parts[0], parts[1]
    return raw, ''


def is_complete_verb_card(card):
    required = {'de', 'infinitive', 'ru', 'cases', 'level', 'conjugation', 'example_de', 'example_ru'}
    if set(card) != required:
        return False
    if not all(card[key] for key in ['de', 'infinitive', 'ru', 'cases', 'level', 'example_de', 'example_ru']):
        return False
    if set(card['conjugation']) != set(CONJUGATION_KEYS):
        return False
    return all(card['conjugation'][key] for key in CONJUGATION_KEYS)


def import_new_verbs(max_imports=MAX_IMPORTS_PER_RUN):
    if not NEW_VERBS_PATH.exists():
        return []

    verbs = json.loads(PUBLIC_VERBS_PATH.read_text(encoding='utf8'))
    existing = {(v.get('de') or '').lower() for v in verbs}
    existing |= {(v.get('infinitive') or '').lower() for v in verbs}

    lines = NEW_VERBS_PATH.read_text(encoding='utf8').splitlines()
    remaining = []
    added = []
    skipped_unknown = []

    for line in lines:
        parsed = parse_line(line)
        if parsed is None:
            remaining.append(line)
            continue

        de, _ru_hint = parsed
        key = de.lower()
        card = VERB_DATA.get(key)

        if key in existing or (card and card['infinitive'].lower() in existing) or (card and card['de'].lower() in existing):
            continue

        if not card:
            remaining.append(line)
            skipped_unknown.append(de)
            continue

        if not is_complete_verb_card(card):
            raise ValueError(f'Incomplete verb card for {de}')

        if len(added) < max_imports:
            verbs.append(card)
            existing.add(card['de'].lower())
            existing.add(card['infinitive'].lower())
            added.append(card['de'])
        else:
            remaining.append(line)

    if added:
        verbs.sort(key=lambda v: v['de'].lower())
        PUBLIC_VERBS_PATH.write_text(json.dumps(verbs, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

    NEW_VERBS_PATH.write_text('\n'.join(remaining) + ('\n' if remaining else ''), encoding='utf8')

    if skipped_unknown:
        print('Skipped verbs without curated full data:', ', '.join(skipped_unknown[:20]))
        if len(skipped_unknown) > 20:
            print(f'... and {len(skipped_unknown) - 20} more')

    return added


if __name__ == '__main__':
    added = import_new_verbs()
    if added:
        print('Imported:', added)
    else:
        print('No new verbs imported')
