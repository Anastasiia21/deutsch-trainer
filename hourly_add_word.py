import json
import os
from pathlib import Path

from import_new_verbs import VERB_DATA, import_new_verbs

VERBS_PATH = Path('public/verbs.json')
NEW_VERBS_PATH = Path('new_verbs.txt')
FALLBACK_LEVELS = {'A1', 'A2'}


def card(de, ru, cases, level, conjugation, example_de, example_ru, infinitive=None):
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


# High-frequency A1/A2 daily-life fallback verbs. These are used only when
# new_verbs.txt has no importable curated verb for this run.
FALLBACK_VERB_DATA = {
    'stehen': card(
        'stehen', 'стоять', ['Nominativ'], 'A1',
        {'ich': 'stehe', 'du': 'stehst', 'er/sie/es': 'steht', 'wir': 'stehen', 'ihr': 'steht', 'sie/Sie': 'stehen'},
        'Ich stehe am Fenster.', 'Я стою у окна.'
    ),
    'sitzen': card(
        'sitzen', 'сидеть', ['Nominativ'], 'A1',
        {'ich': 'sitze', 'du': 'sitzt', 'er/sie/es': 'sitzt', 'wir': 'sitzen', 'ihr': 'sitzt', 'sie/Sie': 'sitzen'},
        'Wir sitzen im Wohnzimmer.', 'Мы сидим в гостиной.'
    ),
    'schlafen': card(
        'schlafen', 'спать', ['Nominativ'], 'A1',
        {'ich': 'schlafe', 'du': 'schläfst', 'er/sie/es': 'schläft', 'wir': 'schlafen', 'ihr': 'schlaft', 'sie/Sie': 'schlafen'},
        'Er schläft tief.', 'Он крепко спит.'
    ),
    'öffnen': card(
        'öffnen', 'открывать', ['Akkusativ'], 'A1',
        {'ich': 'öffne', 'du': 'öffnest', 'er/sie/es': 'öffnet', 'wir': 'öffnen', 'ihr': 'öffnet', 'sie/Sie': 'öffnen'},
        'Sie öffnet das Fenster.', 'Она открывает окно.'
    ),
    'schließen': card(
        'schließen', 'закрывать', ['Akkusativ'], 'A1',
        {'ich': 'schließe', 'du': 'schließt', 'er/sie/es': 'schließt', 'wir': 'schließen', 'ihr': 'schließt', 'sie/Sie': 'schließen'},
        'Ich schließe die Tür.', 'Я закрываю дверь.'
    ),
    'warten': card(
        'warten', 'ждать', ['Akkusativ'], 'A1',
        {'ich': 'warte', 'du': 'wartest', 'er/sie/es': 'wartet', 'wir': 'warten', 'ihr': 'wartet', 'sie/Sie': 'warten'},
        'Wir warten auf den Bus.', 'Мы ждем автобус.'
    ),
    'bezahlen': card(
        'bezahlen', 'платить', ['Akkusativ'], 'A1',
        {'ich': 'bezahle', 'du': 'bezahlst', 'er/sie/es': 'bezahlt', 'wir': 'bezahlen', 'ihr': 'bezahlt', 'sie/Sie': 'bezahlen'},
        'Ich bezahle die Rechnung.', 'Я оплачиваю счет.'
    ),
    'helfen': card(
        'helfen', 'помогать', ['Dativ'], 'A1',
        {'ich': 'helfe', 'du': 'hilfst', 'er/sie/es': 'hilft', 'wir': 'helfen', 'ihr': 'helft', 'sie/Sie': 'helfen'},
        'Er hilft seiner Schwester.', 'Он помогает своей сестре.'
    ),
    'kochen': card(
        'kochen', 'готовить', ['Akkusativ'], 'A1',
        {'ich': 'koche', 'du': 'kochst', 'er/sie/es': 'kocht', 'wir': 'kochen', 'ihr': 'kocht', 'sie/Sie': 'kochen'},
        'Sie kocht das Abendessen.', 'Она готовит ужин.'
    ),
    'putzen': card(
        'putzen', 'убирать', ['Akkusativ'], 'A1',
        {'ich': 'putze', 'du': 'putzt', 'er/sie/es': 'putzt', 'wir': 'putzen', 'ihr': 'putzt', 'sie/Sie': 'putzen'},
        'Ich putze das Fenster.', 'Я мою окно.'
    ),
    'laufen': card(
        'laufen', 'бежать', ['Nominativ'], 'A1',
        {'ich': 'laufe', 'du': 'läufst', 'er/sie/es': 'läuft', 'wir': 'laufen', 'ihr': 'lauft', 'sie/Sie': 'laufen'},
        'Wir laufen im Park.', 'Мы бегаем в парке.'
    ),
    'suchen': card(
        'suchen', 'искать', ['Akkusativ'], 'A1',
        {'ich': 'suche', 'du': 'suchst', 'er/sie/es': 'sucht', 'wir': 'suchen', 'ihr': 'sucht', 'sie/Sie': 'suchen'},
        'Ich suche meine Schlüssel.', 'Я ищу свои ключи.'
    ),
    'duschen': card(
        'duschen', 'принимать душ', ['Nominativ'], 'A1',
        {'ich': 'dusche', 'du': 'duschst', 'er/sie/es': 'duscht', 'wir': 'duschen', 'ihr': 'duscht', 'sie/Sie': 'duschen'},
        'Ich dusche am Morgen.', 'Я принимаю душ утром.'
    ),
    'ankleiden': card(
        'ankleiden', 'одеваться', ['Akkusativ'], 'A1',
        {'ich': 'kleide an', 'du': 'kleidest an', 'er/sie/es': 'kleidet an', 'wir': 'kleiden an', 'ihr': 'kleidet an', 'sie/Sie': 'kleiden an'},
        'Ich kleide mein Kind an.', 'Я одеваю своего ребенка.'
    ),
    'einkaufen': card(
        'einkaufen', 'покупать', ['Akkusativ'], 'A1',
        {'ich': 'kaufe ein', 'du': 'kaufst ein', 'er/sie/es': 'kauft ein', 'wir': 'kaufen ein', 'ihr': 'kauft ein', 'sie/Sie': 'kaufen ein'},
        'Wir kaufen Lebensmittel ein.', 'Мы покупаем продукты.'
    ),
    'vorbereiten': card(
        'vorbereiten', 'готовить', ['Akkusativ'], 'A1',
        {'ich': 'bereite vor', 'du': 'bereitest vor', 'er/sie/es': 'bereitet vor', 'wir': 'bereiten vor', 'ihr': 'bereitet vor', 'sie/Sie': 'bereiten vor'},
        'Sie bereitet das Frühstück vor.', 'Она готовит завтрак.'
    ),
    'telefonieren': card(
        'telefonieren', 'звонить', ['Nominativ'], 'A1',
        {'ich': 'telefoniere', 'du': 'telefonierst', 'er/sie/es': 'telefoniert', 'wir': 'telefonieren', 'ihr': 'telefoniert', 'sie/Sie': 'telefonieren'},
        'Ich telefoniere mit meiner Mutter.', 'Я звоню маме.'
    ),
    'mitnehmen': card(
        'mitnehmen', 'взять с собой', ['Akkusativ'], 'A1',
        {'ich': 'nehme mit', 'du': 'nimmst mit', 'er/sie/es': 'nimmt mit', 'wir': 'nehmen mit', 'ihr': 'nehmt mit', 'sie/Sie': 'nehmen mit'},
        'Ich nehme meinen Kaffee mit.', 'Я беру с собой кофе.'
    ),
    'abwaschen': card(
        'abwaschen', 'мыть посуду', ['Akkusativ'], 'A1',
        {'ich': 'wasche ab', 'du': 'wäschst ab', 'er/sie/es': 'wäscht ab', 'wir': 'waschen ab', 'ihr': 'wascht ab', 'sie/Sie': 'waschen ab'},
        'Ich wasche das Geschirr ab.', 'Я мою посуду.'
    ),
    'entspannen': card(
        'entspannen', 'отдыхать', ['Nominativ'], 'A1',
        {'ich': 'entspanne', 'du': 'entspannst', 'er/sie/es': 'entspannt', 'wir': 'entspannen', 'ihr': 'entspannt', 'sie/Sie': 'entspannen'},
        'Wir entspannen uns am Abend.', 'Мы отдыхаем вечером.'
    ),
}


def meaningful_queue_lines():
    if not NEW_VERBS_PATH.exists():
        return []
    return [line.strip() for line in NEW_VERBS_PATH.read_text(encoding='utf8').splitlines() if line.strip() and not line.strip().startswith('#')]


def write_summary(message):
    print(message)
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_path:
        with open(summary_path, 'a', encoding='utf8') as summary:
            summary.write('### Deutsch Trainer vocabulary automation\n\n')
            summary.write(message + '\n')


def add_fallback_a1_a2_verb():
    verbs = json.loads(VERBS_PATH.read_text(encoding='utf8'))
    existing = {(v.get('de') or '').lower() for v in verbs}
    existing |= {(v.get('infinitive') or '').lower() for v in verbs}

    # Prefer simple daily-life verbs, then any curated A1/A2 verb from import_new_verbs.py.
    fallback_cards = list(FALLBACK_VERB_DATA.values())
    fallback_cards.extend(card for card in VERB_DATA.values() if card.get('level') in FALLBACK_LEVELS)

    seen = set()
    for fallback_card in fallback_cards:
        key = (fallback_card.get('infinitive') or fallback_card.get('de') or '').lower()
        de_key = (fallback_card.get('de') or '').lower()
        if key in seen or de_key in seen:
            continue
        seen.add(key)
        seen.add(de_key)
        if key in existing or de_key in existing:
            continue

        verbs.append(fallback_card)
        verbs.sort(key=lambda v: (v.get('de') or '').lower())
        VERBS_PATH.write_text(json.dumps(verbs, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
        write_summary(f"Added fallback {fallback_card.get('level', 'A1/A2')} verb: {fallback_card['de']}")
        return fallback_card['de']

    queue_lines = meaningful_queue_lines()
    if queue_lines:
        write_summary(
            'No vocabulary added: new_verbs.txt has entries, but none were importable with curated full data, '
            'and all fallback A1/A2 verbs are already present.'
        )
    else:
        write_summary(
            'No vocabulary added: new_verbs.txt is empty, and the main A1/A2 fallback verbs are already present.'
        )
    return None


def main():
    added_from_queue = import_new_verbs()
    if added_from_queue:
        write_summary('Imported new verb from new_verbs.txt: ' + ', '.join(added_from_queue))
        return

    add_fallback_a1_a2_verb()


if __name__ == '__main__':
    main()
