from pathlib import Path
import fitz,json,hashlib,shutil,math,unicodedata
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[3];qa=root/'tmp/pdfs/experiment-aligned-20260923/singlecol-dual';qa.mkdir(parents=True,exist_ok=True)
result=json.loads((root/'tmp/pdfs/experiment-aligned-20260923/singlecol-translation-result.json').read_text())
p=next(Path(x) for x in result['filePaths'] if 'LR_dual' in x)
doc=fitz.open(p);clean=fitz.open(root/'output/pdf/main.pdf');assert len(doc)==len(clean)==5
import runpy
runpy.run_path(str(root/'paper/audits/experiment-aligned-rewrite-20260923/repair-chinese.py'))['repair'](doc,clean)
ann=json.loads((root/'paper/audits/experiment-aligned-rewrite-20260923/highlights.json').read_text())['annotations']
canon=lambda s:''.join(c.lower() for c in unicodedata.normalize('NFKD',s) if c.isalnum())
for i,(cp,dp) in enumerate(zip(clean,doc)):
 assert abs(dp.rect.width-2*cp.rect.width)<1
 assert canon(cp.get_text())==canon(dp.get_text(clip=cp.rect)),i
for r in ann:
 page=doc[r['page']-1]
 a=page.add_highlight_annot([fitz.Rect(q).quad for q in r['rects']]);a.set_colors(stroke=(1,.4,.4));a.set_opacity(.35);a.set_info(title='Codex · 原版差异 · 2026-09-23',content=r['comment']);a.update()
out=root/'output/pdf/main-bilingual-en-zh.pdf';doc.save(out,garbage=4,deflate=True);doc.close();doc=fitz.open(out)
assert sum(len(list(p.annots() or [])) for p in doc)==len(ann)
sheet=Image.new('RGB',(1244,421*math.ceil(len(doc)/2)),'white')
for i,p in enumerate(doc):
 pix=p.get_pixmap(matrix=fitz.Matrix(1.1,1.1));pix.save(qa/f'dual-{i+1}.png');im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((602,390));tile=Image.new('RGB',(622,421),'#eee');tile.paste(im,(10,22));ImageDraw.Draw(tile).text((10,5),f'Page {i+1}',fill='black');sheet.paste(tile,((i%2)*622,(i//2)*421))
sheet.save(qa/'contact.png')
# Render clean red comparison as well.
high=fitz.open(root/'output/pdf/main-revision-highlighted.pdf')
for i in range(len(high)):high[i].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(qa/f'highlight-{i+1}.png')
name='最新双语-实验主线与单栏表格-红色对比-20260923.pdf';target=root/'tmp/pdfs/zotero-final-comparison-20260922'/name;shutil.copy2(out,target)
files={}
for name in ['main.pdf','main-revision-highlighted.pdf','main-bilingual-en-zh.pdf','main-overleaf-original-20260921.pdf']:
 p=root/'output/pdf'/name;d=fitz.open(p);files[name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pages':len(d),'annotations':sum(len(list(p.annots() or [])) for p in d)}
record={'baseline_commit':'121a6182b','translation':{'plugin':'Zotero PDF2zh 4.1.7','engine':'pdf2zh_next','service':'siliconflowfree','task_id':'c7c49646-f210-407c-9d20-61a1ea9c7100','mode':'English left / Chinese right','result':result},'files':files,'validation':{'english_text_identical_to_clean':True,'red_highlights':len(ann),'english_side_only':True,'clean_pages':5,'undefined_references':0,'overfull_boxes':0,'underfull_boxes':0},'zotero':{'status':'pending import','import_path':str(target)}}
(root/'paper/audits/experiment-aligned-rewrite-20260923/bilingual-zotero.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(files,indent=2))
