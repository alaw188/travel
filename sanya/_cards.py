# -*- coding: utf-8 -*-
import io, re

s = io.open('index.html', encoding='utf-8').read()
cards = re.findall(
    r'<figure class="spot__fig"[^>]*data-label="([^"]*)">\s*<img class="spot__img" src="([^"]*)"',
    s, re.S)
GEN = ('Wenchang', 'Steamed', 'Dim_sum', 'Georgia_Aquarium', 'Marriott_Hotel_Lima',
       'Shrimp', 'coffee', 'A_small_cup', 'Cantonese', 'white_cut', 'qingbuliang',
       'Hainanese_chicken', 'siem_reap', 'Weissbier', 'Aquarium_-_Ocean',
       'Sanya_Beach_Night')
print('=== figure/img list ===')
for label, src in cards:
    tag = 'GENERIC' if any(k in src for k in GEN) else 'real'
    print('%-8s %-22s %s' % (tag, label, src[-50:]))
