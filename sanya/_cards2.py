# -*- coding: utf-8 -*-
import io, re

s = io.open('index.html', encoding='utf-8').read()
arts = re.findall(
    r'<article class="card spot[^"]*"[^>]*>.*?data-label="([^"]*)">\s*<img[^>]*src="([^"]*)".*?<h4>(.*?)</h4>',
    s, re.S)
GEN = ('Wenchang_Chicken_1', 'Steamed_fish_October', 'Dim_sum_collection',
       'Georgia_Aquarium', 'Marriott_Hotel_Lima', 'four_types_of_Shrimp',
       'A_small_cup_of_coffee', 'Cantonese_restaurant', 'white_cut_chicken',
       'Hainanese_chicken_rice', 'siem_reap', 'Weissbier_Munich',
       'Ocean_Voyager_Tunnel', 'Sanya_Beach_Night')
for label, src, h4 in arts:
    tag = 'GENERIC' if any(k in src for k in GEN) else 'real   '
    title = re.sub(r'<[^>]+>', '', h4).strip()
    print('%s | %-18s | %s' % (tag, label, title[:40]))
