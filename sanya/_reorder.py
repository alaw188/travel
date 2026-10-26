# -*- coding: utf-8 -*-
"""Reorder the 餐廳與美食 spot cards by itinerary day."""
import io, re

P = 'index.html'
s = io.open(P, encoding='utf-8').read()

ORDER = ['MAYAN', '嗲嗲的椰子雞', '鄉村海味', '老漁民', '濤·海底', 'ZRS藍',
         '天府中餐廳', '天津灣', 'SEACAVE', '林姐']

m = re.search(r'(<h3 class="group[^"]*">餐廳與美食.*?</h3>\s*<div class="spots">)(.*?)(\n    </div>)', s, re.S)
assert m, 'restaurant group not found'
body = m.group(2)
arts = re.findall(r'      <article class="card spot.*?</article>', body, re.S)
assert len(arts) == len(ORDER), (len(arts), len(ORDER))

titles = []
for a in arts:
    t = re.search(r'<h4>(.*?)</h4>', a, re.S).group(1)
    titles.append(' '.join(re.sub(r'<[^>]+>', '', t).split()))

idx = []
for w in ORDER:
    hits = [i for i, t in enumerate(titles) if w in t and i not in idx]
    assert len(hits) == 1, (w, hits, titles)
    idx.append(hits[0])

new_body = '\n\n' + '\n\n'.join(arts[i].strip() for i in idx)
s = s[:m.start(2)] + new_body + s[m.end(2):]
io.open(P, 'w', encoding='utf-8', newline='').write(s)

print('old order:')
for t in titles:
    print('   ', t)
print('new order:')
for i in idx:
    print('   ', titles[i])
