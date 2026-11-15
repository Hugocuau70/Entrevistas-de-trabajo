from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

ROOT=Path(__file__).resolve().parents[1]
r=Presentation(); r.slide_width=Inches(13.333); r.slide_height=Inches(7.5)
C={'ink':'202124','muted':'5F6368','blue':'174EA6','accent':'4285F4','green':'34A853','yellow':'FBBC05','red':'EA4335','surface':'F8F9FA','line':'DADCE0'}
def box(s,x,y,w,h,color):
 a=s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)); a.fill.solid(); a.fill.fore_color.rgb=RGBColor.from_string(C.get(color,color)); a.line.fill.background(); return a

def txt(s,x,y,w,h,text,size=22,color='ink',bold=False):
 a=s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); f=a.text_frame; f.word_wrap=True
 for i,line in enumerate(text.split('\n')):
  p=f.paragraphs[0] if i==0 else f.add_paragraph(); p.text=line; p.font.name='DejaVu Sans'; p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=RGBColor.from_string(C.get(color,color)); p.space_after=Pt(12)
 return a

def slide(title,kicker):
 s=r.slides.add_slide(r.slide_layouts[6]); box(s,0,0,13.333,.07,'accent')
 txt(s,.65,.35,12,.3,kicker.upper(),11,'blue',True); txt(s,.65,.93,12,1.05,title,30,'ink',True)
 box(s,.65,6.91,12,.012,'line'); txt(s,.65,7.02,11,.25,'WORKING TEMPLATE  |  Mexico  |  H1 2027  |  Assumptions pending validation',10,'muted')
 txt(s,12.1,7.02,.55,.25,str(len(r.slides)),10,'muted')
 return s
s=slide('A focused growth plan for H1 2027','Uber for Business • Interview preparation')
txt(s,.65,2.25,10,1.5,'[Selected account]\nCorporate mobility and employee meals',30)
txt(s,.65,4.5,10,.8,'Diego  |  Mid Market Account Executive case',20,'muted')
for i,c in enumerate(['accent','green','yellow','red']): box(s,.65+i*.65,5.8,.45,.12,c)
s=slide('Choose the account before building the forecast','Account selection • Discussion worksheet')
for i,(title,body,c) in enumerate([
 ('Eligible company','250–2,500 employees globally\nDocumented operations in Mexico','accent'),
 ('Recurring demand','Employee travel with a clear purpose\nA distinct corporate meals use case','green'),
 ('Timely activation','Evidence of an H1 demand trigger\nA feasible buying and launch process','yellow')]):
 x=.65+i*4.08; box(s,x,2.35,3.85,3.55,'surface'); box(s,x,2.35,3.85,.06,c); txt(s,x+.2,2.65,3.45,.7,title,21,'ink',True); txt(s,x+.2,3.55,3.45,2,body,19,'muted')
s=slide('Separate evidence from planning assumptions','Research standards • To complete together')
for y,label,body,c in [(2.2,'Verified fact','Source, publication date, scope and supporting passage.','green'),(3.65,'Planning assumption','Rationale, range and effect on the forecast.','accent'),(5.1,'To validate','Discovery question, owner and decision affected.','yellow')]:
 box(s,.65,y,.08,1.05,c); txt(s,.95,y,3.5,.55,label,23,'ink',True); txt(s,4.5,y,8,1,body,21,'muted')
s=slide('Model actual usage from activation through June','Forecast design • No account assumptions selected')
txt(s,.65,2.15,12,.8,'Monthly GB = completed rides × $10 + Eats orders × $15',25,'blue',True)
txt(s,.65,3.35,12,2.2,'1. Define eligible users and the activities that create demand.\n2. Set activation timing, adoption and monthly frequency.\n3. Sum Jan–Jun usage and test a slower activation scenario.',22)
txt(s,.65,6,12,.5,'Case inputs: $350,000 H1 quota; $10 per ride; $15 per Eats order. All amounts in USD.',12,'muted')
for s in r.slides:
 s.notes_slide.notes_text_frame.text='Plantilla de trabajo. Completar con las decisiones de Diego y evidencia verificable. No presentar como propuesta final.'
out=ROOT/'presentacion/plantilla-trabajo.pptx'; r.save(out)
check=Presentation(out)
assert len(check.slides)==4
for s in check.slides:
 for sh in s.shapes:
  assert sh.left>=0 and sh.top>=0 and sh.left+sh.width<=r.slide_width and sh.top+sh.height<=r.slide_height
print(out)
