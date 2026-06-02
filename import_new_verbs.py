import json
from pathlib import Path

NEW_VERBS_PATH = Path('new_verbs.txt')
PUBLIC_VERBS_PATH = Path('public/verbs.json')

SEPARATORS = ['-', '—', ':', '\t']


def parse_line(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    for sep in SEPARATORS:
        if sep in line:
            parts = [p.strip() for p in line.split(sep, 1)]
            if len(parts) == 2 and parts[0]:
                return parts[0], parts[1]
    return line, ''


def build_verb(de, ru=''):
    infinitive = de
    fallback = infinitive
    return {
        'de': de,
        'infinitive': infinitive,
        'ru': ru,
        'cases': ['Nominativ'],
        'level': 'A2',
        'conjugation': {
            'ich': fallback,
            'du': fallback,
            'er/sie/es': fallback,
            'wir': fallback,
            'ihr': fallback,
            'sie/Sie': fallback,
        },
        'example_de': '',
        'example_ru': ''
    }


def import_new_verbs():
    if not NEW_VERBS_PATH.exists():
        return []

    verbs = json.loads(PUBLIC_VERBS_PATH.read_text(encoding='utf8'))
    existing = {v['de'].lower() for v in verbs}

    lines = NEW_VERBS_PATH.read_text(encoding='utf8').splitlines()
    remaining = []
    added = []

    for line in lines:
        parsed = parse_line(line)
        if parsed is None:
            remaining.append(line)
            continue
        de, ru = parsed
        if de.lower() in existing:
            continue
        verbs.append(build_verb(de, ru))
        existing.add(de.lower())
        added.append(de)

    if added:
        verbs.sort(key=lambda v: v['de'].lower())
        PUBLIC_VERBS_PATH.write_text(json.dumps(verbs, ensure_ascii=False, indent=2), encoding='utf8')

    NEW_VERBS_PATH.write_text('\n'.join(remaining) + ('\n' if remaining else ''), encoding='utf8')
    return added


if __name__ == '__main__':
    added = import_new_verbs()
    if added:
        print('Imported:', added)
    else:
        print('No new verbs imported')
