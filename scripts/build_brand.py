"""Generate original vector artwork and matching PNGs. Development-only: Pillow."""
from __future__ import annotations

import argparse
import html
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
NAVY, TEAL, CORAL, PAPER, MUTED = '#132D38', '#087F8C', '#F07167', '#F5F8F6', '#526B75'


def font_path(bold=False):
    env = os.environ.get('PROMPTHARBOR_FONT_BOLD' if bold else 'PROMPTHARBOR_FONT')
    options = [env] if env else []
    options += ([r'C:/Windows/Fonts/segoeuib.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
                if bold else [r'C:/Windows/Fonts/segoeui.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    return next((p for p in options if Path(p).is_file()), None)


class Scene:
    def __init__(self, w, h, background=None, title='PromptHarbor'):
        self.w, self.h, self.scale = w, h, 3
        self.im = Image.new('RGBA', (w*3, h*3), background or (0,0,0,0))
        self.draw = ImageDraw.Draw(self.im)
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">',
                    f'<title>{html.escape(title)}</title>']
        if background:
            self.svg.append(f'<rect width="{w}" height="{h}" fill="{background}"/>')

    def rect(self, x,y,w,h,color,r=0):
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{color}"/>')
        self.draw.rounded_rectangle((x*3,y*3,(x+w)*3,(y+h)*3),radius=r*3,fill=color)

    def circle(self,x,y,r,color):
        self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
        self.draw.ellipse(((x-r)*3,(y-r)*3,(x+r)*3,(y+r)*3),fill=color)

    def line(self,points,color,width):
        value=' '.join(f'{x:.3f},{y:.3f}' for x,y in points)
        self.svg.append(f'<polyline points="{value}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
        self.draw.line([(round(x*3),round(y*3)) for x,y in points],fill=color,width=round(width*3),joint='curve')
        for x,y in (points[0],points[-1]):
            r=width/2
            self.draw.ellipse(((x-r)*3,(y-r)*3,(x+r)*3,(y+r)*3),fill=color)

    def text(self,x,y,value,size,color=NAVY,bold=False):
        self.svg.append(f'<text x="{x}" y="{y}" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{html.escape(value)}</text>')
        selected=font_path(bold)
        font=ImageFont.truetype(selected,size*3) if selected else ImageFont.load_default(size=size*3)
        self.draw.text((x*3,y*3),value,font=font,fill=color,anchor='ls')

    def save(self,path, png=True):
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        path.with_suffix('.svg').write_text('\n'.join(self.svg+['</svg>'])+'\n',encoding='utf-8')
        if png:
            self.im.resize((self.w,self.h),Image.Resampling.LANCZOS).save(path.with_suffix('.png'))


def cubic(a,b,c,d):
    return [tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k] for k in (0,1))
            for t in [i/32 for i in range(33)]]


def mark(s,x,y,scale=1,color=TEAL):
    def pts(values):return [(x+a*scale,y+b*scale) for a,b in values]
    harbor=cubic((44,130),(44,182),(76,216),(128,216))+cubic((128,216),(180,216),(212,182),(212,130))[1:]
    s.line(pts(harbor),color,18*scale)
    s.line(pts([(66,63),(66,97),(128,139),(128,178)]),color,18*scale)
    s.line(pts([(190,63),(190,97),(128,139)]),color,18*scale)
    s.line(pts([(128,40),(128,94)]),color,18*scale)
    s.circle(x+128*scale,y+139*scale,13*scale,CORAL)


def build():
    dest=ROOT/'assets/brand'
    logo=Scene(256,256,title='PromptHarbor logo: three task routes meet inside an open harbor')
    mark(logo,0,0);logo.save(dest/'logo')
    dark=Scene(256,256,title='PromptHarbor logo for dark backgrounds')
    mark(dark,0,0,color='#8DD4D0');dark.save(dest/'logo-dark')
    avatar=Scene(512,512,PAPER)
    mark(avatar,64,64,1.5);avatar.save(dest/'avatar')
    hero=Scene(1200,340,PAPER)
    mark(hero,55,40,1)
    hero.text(355,93,'TASK  /  MODEL  /  DELIVERY',15,TEAL,True)
    hero.text(350,174,'PromptHarbor',65,NAVY,True)
    hero.text(354,222,'Understand the work. Choose the model.',24,MUTED)
    hero.text(354,258,'Bring the pieces together.',24,MUTED)
    hero.save(dest/'hero')
    social=Scene(1280,640,PAPER)
    social.rect(0,0,12,640,TEAL)
    social.text(80,104,'AN OPEN AGENT SKILL',19,TEAL,True)
    social.text(76,226,'PromptHarbor',78,NAVY,True)
    social.text(80,297,'The right models for your work.',32,MUTED)
    social.text(80,353,'One question. Or a whole project.',27,MUTED)
    social.rect(80,423,624,83,'#E4EFEB',15)
    social.text(104,459,'Understand  →  Recommend  →  Coordinate',22,TEAL,True)
    social.text(104,489,'Evidence-backed choices. Shared interfaces.',18,MUTED)
    mark(social,891,200,1.1)
    social.text(80,589,'MODEL ADVICE + COPYABLE HANDOFFS',16,MUTED,True)
    social.save(dest/'social-preview')
    skill=ROOT/'skills/promptharbor/assets';skill.mkdir(parents=True,exist_ok=True)
    for name in ('logo.svg','avatar.png'):
        (skill/name).write_bytes((dest/name).read_bytes())
    # Compact visual QA contact sheet; not a README asset.
    sheet=Image.new('RGB',(1200,1040),'#FFFFFF')
    sheet.paste(hero.im.resize((1200,340),Image.Resampling.LANCZOS),(0,0))
    sheet.paste(social.im.resize((960,480),Image.Resampling.LANCZOS),(120,365))
    for px in (24,48,96,128):
        thumb=logo.im.resize((px,px),Image.Resampling.LANCZOS)
        sheet.paste(thumb,(60+px*4,880),thumb)
    out=ROOT/'out';out.mkdir(exist_ok=True)
    sheet.save(out/'brand-review.png')


if __name__=='__main__':
    build()
