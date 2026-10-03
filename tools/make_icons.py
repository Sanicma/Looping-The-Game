# Genera el ícono LED de Looping. Uso: python3 tools/make_icons.py [assets|android]
import sys,os,math,colorsys
from PIL import Image,ImageDraw,ImageFilter
def grad(S):
    im=Image.new('RGBA',(S,S));d=ImageDraw.Draw(im)
    for y in range(S):
        t=y/S;d.line([(0,y),(S,y)],fill=(int(24-12*t),int(30-15*t),int(50-23*t),255))
    return im
def mark(S,scale):
    cx=cy=S/2;a=S*scale/2;N=720;lw=max(2,int(S*.04))
    pts=[(cx+a*math.cos(u)/(1+math.sin(u)**2),cy+a*.95*math.sin(u)*math.cos(u)/(1+math.sin(u)**2)) for u in [i/N*2*math.pi for i in range(N+1)]]
    L=Image.new('RGBA',(S,S),(0,0,0,0));C=Image.new('RGBA',(S,S),(0,0,0,0));dl=ImageDraw.Draw(L);dc=ImageDraw.Draw(C);cw=max(1,int(lw*.34))
    for i in range(N):
        h=(195+130*math.sin(math.pi*i/N))%360
        r,g,b=[int(c*255) for c in colorsys.hsv_to_rgb(h/360,.75,1)]
        dl.line([pts[i],pts[i+1]],fill=(r,g,b,255),width=lw);x,y=pts[i];dl.ellipse([x-lw/2,y-lw/2,x+lw/2,y+lw/2],fill=(r,g,b,255))
        dc.line([pts[i],pts[i+1]],fill=(255,255,255,215),width=cw);dc.ellipse([x-cw/2,y-cw/2,x+cw/2,y+cw/2],fill=(255,255,255,215))
    big=L.filter(ImageFilter.GaussianBlur(S*.05));small=L.filter(ImageFilter.GaussianBlur(S*.016))
    out=Image.new('RGBA',(S,S),(0,0,0,0))
    for g in (big,big,small):out.alpha_composite(g)
    out.alpha_composite(L);out.alpha_composite(C);return out
def make(size,scale,bg,ss=2):
    S=size*ss;im=grad(S) if bg else Image.new('RGBA',(S,S),(0,0,0,0));im.alpha_composite(mark(S,scale))
    return im.resize((size,size),Image.LANCZOS) if ss>1 else im
def circle(im):
    m=Image.new('L',im.size,0);ImageDraw.Draw(m).ellipse([0,0,im.size[0]-1,im.size[1]-1],fill=255);im.putalpha(m);return im
mode=sys.argv[1] if len(sys.argv)>1 else 'android'
if mode=='assets':
    A='assets';os.makedirs(A,exist_ok=True)
    make(1024,.74,True).save(A+'/icon-only.png');make(1024,.5,False).save(A+'/icon-foreground.png');grad(1024).save(A+'/icon-background.png')
    sp=make(2732,.34,True,ss=1);sp.save(A+'/splash.png');sp.save(A+'/splash-dark.png')
else:
    R='android/app/src/main/res'
    for d,px in {'mdpi':48,'hdpi':72,'xhdpi':96,'xxhdpi':144,'xxxhdpi':192}.items():
        D=f'{R}/mipmap-{d}';os.makedirs(D,exist_ok=True)
        sq=make(px,.78,True);sq.save(D+'/ic_launcher.png');circle(sq.copy()).save(D+'/ic_launcher_round.png')
        make(round(px*2.25),.5,False).save(D+'/ic_launcher_foreground.png')
    os.makedirs(R+'/mipmap-anydpi-v26',exist_ok=True);os.makedirs(R+'/values',exist_ok=True)
    xml='<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n    <background android:drawable="@color/ic_launcher_background"/>\n    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n</adaptive-icon>\n'
    for n in ('ic_launcher','ic_launcher_round'):open(f'{R}/mipmap-anydpi-v26/{n}.xml','w').write(xml)
    open(R+'/values/ic_launcher_background.xml','w').write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#0D111D</color>\n</resources>\n')
print('listo',mode)
