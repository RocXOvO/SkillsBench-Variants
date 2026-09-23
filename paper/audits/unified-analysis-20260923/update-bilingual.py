from pathlib import Path
import subprocess,fitz,re,json,hashlib
R=Path(__file__).resolve().parents[3];A=Path(__file__).parent;Q=R/'tmp/pdfs/unified-analysis-20260923';F=Path('/Users/duchongyang/.cache/babeldoc/fonts')
old=fitz.open(Q/'renumbered.pdf');en=fitz.open(R/'output/pdf/main.pdf');d=fitz.open()
for i in range(len(en)):
 p=d.new_page(width=1224,height=792);p.show_pdf_page(fitz.Rect(0,0,612,792),en,i)
 if i==4:p.show_pdf_page(fitz.Rect(612,0,1224,792),en,i)
 elif i!=3:p.show_pdf_page(fitz.Rect(612,0,1224,792),old,i,clip=fitz.Rect(612,0,1224,792))
 else:
  p.show_pdf_page(fitz.Rect(612,0,927,414),old,i,clip=fitz.Rect(612,0,927,414))
  p.show_pdf_page(fitz.Rect(612,414,927,690),old,i,clip=fitz.Rect(612,444,927,720))
  p.show_pdf_page(fitz.Rect(666,692,917,709),old,i,clip=fitz.Rect(927,71,1178,88))
  p.show_pdf_page(fitz.Rect(927,73,1224,695),old,i,clip=fitz.Rect(927,103,1224,725))
norm=lambda t:re.sub(r'\s+','',t)
for i,p in enumerate(d):
 assert norm(p.get_text(clip=fitz.Rect(0,0,612,792)))==norm(en[i].get_text())
 assert not list(p.annots() or [])
d.save(R/'output/pdf/main-bilingual-en-zh.pdf',garbage=4,deflate=True)
d=fitz.open(R/'output/pdf/main-bilingual-en-zh.pdf')
for i,p in enumerate(d):p.get_pixmap(matrix=fitz.Matrix(1.15,1.15),clip=fitz.Rect(612,0,1224,792)).save(Q/f'zh-{i+1}.png')
for i,p in enumerate(d):
 assert norm(p.get_text(clip=fitz.Rect(0,0,612,792)))==norm(en[i].get_text())
 assert not list(p.annots() or [])
text='\n'.join(p.get_text() for p in en)
assert '4. ANALYSIS' in text and '3. EXPERIMENTS' in text
assert 'LOCATING SUCCESSFUL' not in text and 'INTERPRETING GAINS AS EVIDENCE' not in text
report={x:{'pages':len(fitz.open(R/'output/pdf'/x)),'sha256':hashlib.sha256((R/'output/pdf'/x).read_bytes()).hexdigest(),'annotations':0} for x in ['main.pdf','main-bilingual-en-zh.pdf']}
(A/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
