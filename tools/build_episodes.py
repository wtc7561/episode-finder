"""Build site/episodes.json for the Episode Finder from the Airtable CSV export."""
import csv, json, os, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else 'out/airtable_csv'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'site/episodes.json'

def multi(s):
    s = (s or '').strip()
    return [v.strip() for v in next(csv.reader([s]))] if s else []

def short_place(p):
    parts = [x.strip() for x in p.split(',')]
    if parts[-1] == 'United States':
        parts = parts[:-1]
    return ', '.join(parts[:2]) if len(parts) > 2 else ', '.join(parts)

guests = {}
for g in csv.DictReader(open(os.path.join(SRC, '2_Guests.csv'), encoding='utf-8')):
    guests[g['Guest'].strip()] = {'bio': g['Micro-bio'].strip(), 'n': int(g['Number of episodes'] or 0)}

eps = []
for x in csv.DictReader(open(os.path.join(SRC, '1_Episodes.csv'), encoding='utf-8')):
    eps.append({
        'no': x['No.'].strip(),
        'title': x['Title'].strip(),
        'date': x['Published'].strip(),
        'length': x['Length'].strip(),
        'type': multi(x['Episode type']),
        'series': multi(x['Series']),
        'guests': multi(x['Guests']),
        'summary': x['Summary'].strip(),
        'ideas': [l.strip() for l in x['Key ideas'].split('\n') if l.strip()],
        'discipline': multi(x['Discipline']),
        'issues': multi(x['Issues and goals']),
        'settings': multi(x['Settings and communities']),
        'approaches': multi(x['Approaches and practices']),
        'people': multi(x['People discussed']),
        'orgs': multi(x['Organizations']),
        'places': [short_place(p) for p in multi(x['Places'])],
        'repriseOf': x['Reprise of / originally'].strip(),
        'link': x['Listen link'].strip(),
    })
eps.sort(key=lambda e: e['date'], reverse=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({'episodes': eps, 'guests': guests}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(eps), 'episodes,', len(guests), 'guests ->', OUT, os.path.getsize(OUT), 'bytes')
