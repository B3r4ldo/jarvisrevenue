"""Optional offline export of reviewed, deterministic social graphics (requires Pillow)."""
import csv
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')

def font(size, bold=False):
    return ImageFont.truetype(str(FONT_DIR / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')), size)

def export():
    target=ROOT/'commercial/creatives'
    target.mkdir(exist_ok=True)
    rows=list(csv.DictReader((ROOT/'commercial/content-14-days.csv').open(encoding='utf-8-sig')))
    for row in rows:
        image=Image.new('RGB',(1080,1080),'#fffdf9');d=ImageDraw.Draw(image)
        d.rectangle((0,0,1080,120),fill='#103e2e');d.text((55,34),'SeuPetFeliz',font=font(42,True),fill='#f3bf58')
        d.text((55,150),'COMPARE ANTES DE ESCOLHER',font=font(24,True),fill='#95670c')
        y=202
        for line in textwrap.wrap(row['headline'],30):
            d.text((55,y),line,font=font(46,True),fill='#103e2e');y+=59
        ids=row['product_ids'].split(',');n=len(ids);width=270;gap=32;start=(1080-(width*n+gap*(n-1)))//2
        for idx,pid in enumerate(ids):
            p=ROOT/'preview/assets/generated'/f'{pid}.webp'
            im=Image.open(p).convert('RGBA');im.thumbnail((width,330))
            x=start+idx*(width+gap)+(width-im.width)//2
            image.paste(im,(x,460+(330-im.height)//2),im)
        d.rounded_rectangle((55,825,1025,920),radius=28,fill='#edb94d')
        text='Confira o guia no link do perfil'
        d.text((105,850),text,font=font(36,True),fill='#103e2e')
        d.text((55,953),'Publicidade · Imagens ilustrativas geradas por IA.',font=font(22),fill='#53655a')
        d.text((55,988),'Confira a embalagem e a variante na Amazon.',font=font(22),fill='#53655a')
        image.save(target/f'dia-{int(row["day"]):02}.webp',quality=88,method=6)

if __name__=='__main__':
    export()
