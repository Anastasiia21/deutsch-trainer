import json
from pathlib import Path
file_verbs = {v['de'].lower() for v in json.loads(Path('public/verbs.json').read_text(encoding='utf8'))}
user = ['sein','haben','heißen','wohnen','leben','kommen','gehen','fahren','reisen','arbeiten','lernen','sprechen','verstehen','denken','wissen','kennen','lesen','schreiben','sehen','hören','lieben','mögen','träumen','lachen','sich freuen','sich treffen','kaufen','essen','trinken','spielen']
missing = [v for v in user if v.lower() not in file_verbs]
print('missing:', missing)
print('count file:', len(file_verbs))
print('count user unique:', len(set(user)))
