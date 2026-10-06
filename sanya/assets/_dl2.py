# -*- coding: utf-8 -*-
import urllib.request, shutil, os

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"}

jobs = [
    ("cdf-mall.jpg", "https://xqimg.imedao.com/177d3c5e60d79c513fe10bdb.jpeg!800.jpg"),
    ("dxdt.jpg", "https://www.hlhbsc.org/upload/download/Spot_pic/Spot_picfile_000069_New.jpg"),
    ("luhuitou.jpg", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqrPxNWKOVxdZVgKR7_cS30Oo2PSr9alR_sHh-VCoAh5aKBejSVPMg-j2f&s=10"),
    ("xiangcun.webp", "https://ak-d.tripcdn.com/images/1me5t12000buvvoq2A4C8_D_690_460_R5_Q70.jpg_.webp"),
    ("xiaohuzi.jpg", "https://dynamic-media-cdn.tripadvisor.com/media/daodao/photo-o/17/4b/57/75/9.jpg?w=1000&h=-1&s=1"),
    ("skybar.jpg", "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/13/e9/f9/ce/sky-bar.jpg"),
]

for name, url in jobs:
    try:
        req = urllib.request.Request(url, headers=UA)
        data = urllib.request.urlopen(req, timeout=30).read()
        open(name, "wb").write(data)
        print(name, len(data))
    except Exception as e:
        print("FAIL", name, e)

src = r"D:\Downloads\2025112005232664-1024x764.jpg"
shutil.copyfile(src, "tianya-aerial.jpg")
print("tianya-aerial.jpg copied", os.path.getsize("tianya-aerial.jpg"))
