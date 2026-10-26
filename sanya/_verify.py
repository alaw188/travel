# -*- coding: utf-8 -*-
import io, re
s = io.open('index.html', encoding='utf-8').read()
clean = re.sub(r'<script\b.*?</script>', '', s, flags=re.S)
clean = re.sub(r'<style\b.*?</style>', '', clean, flags=re.S)
print('div:', len(re.findall(r'<div\b', clean)), '/', clean.count('</div>'))
print('article:', len(re.findall(r'<article\b', s)), '/', s.count('</article>'))
print('section:', len(re.findall(r'<section', s)), '/', s.count('</section>'))
print('table:', len(re.findall(r'<table\b', s)), '/', s.count('</table>'))
print('tr:', len(re.findall(r'<tr\b', s)), '/', s.count('</tr>'))
print('spot cards:', len(re.findall(r'<article class="card spot', s)))
print('poi cards:', len(re.findall(r'class="poi"', s)))
print('map POIS:', len(re.findall(r"^\s*\{\s*$", re.search(r'var POIS = \[(.*?)\];', s, re.S).group(1), re.M)))
print()
for k in ['海棠灣店', 'Day 2 晚餐', '20:00–22:00', '10 段', '¥340', '162 km', '¥5,145', '¥12,345']:
    n = s.count(k)
    flag = '  <-- CHECK' if n else ''
    print('%-14s %d%s' % (k, n, flag))
