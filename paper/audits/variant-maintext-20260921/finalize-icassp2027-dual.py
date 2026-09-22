from pathlib import Path
import fitz,json,hashlib,shutil,math,unicodedata
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[3];qa=root/'tmp/pdfs/icassp2027/dual';qa.mkdir(parents=True,exist_ok=True)
result=json.loads((root/'tmp/pdfs/icassp2027/translation-result.json').read_text())
p=next(Path(x) for x in result['filePaths'] if 'LR_dual' in x)
doc=fitz.open(p);clean=fitz.open(root/'output/pdf/main.pdf');assert len(doc)==len(clean)==8
ann=json.loads((root/'paper/audits/variant-maintext-20260921/original-comparison-highlights-20260922.json').read_text())['annotations']
canon=lambda s:''.join(c.lower() for c in unicodedata.normalize('NFKD',s) if c.isalnum())
for i,(cp,dp) in enumerate(zip(clean,doc)):
 assert abs(dp.rect.width-2*cp.rect.width)<1
 assert canon(cp.get_text())==canon(dp.get_text(clip=cp.rect)),i
# PDF2zh returned three English fallbacks after backend rate limiting.
# Complete the fallbacks and two malformed Chinese heading/transition lines.
# The English original remains untouched.
translation_repairs=[
 (1,(666.3,413.7,908.8,434.0),'下文实验依次回答这些问题。'),
 (1,(666.3,438.0,908.8,456.0),'3. 诊断技能效用范围'),
 (0,(943.8,471.2,1171.5,509.0),'• 报告规范。我们明确从选定收益到有限范围迁移的各层主张所需的演化来源、对照和支撑材料。'),
 (1,(927.1,511.5,1171.5,603.0),'源任务上的提升并不意味着有效泛化。三种方法在两次源任务运行中的平均奖励均有提升，但变体结果出现分化。SkillEvolver 的平均增益为 11.94 分；SPARK 接近零，为 +0.65 分；CoEvoSkills 则低于无技能基线，为 −5.01 分。SkillEvolver 改善的变体多于退化的变体（47 对 20），而 SPARK 和 CoEvoSkills 相反。因此，后两种方法在源任务上的收益并未转化为变化任务上的一致优势。'),
 (2,(666.3,348.0,1171.5,383.0),'表 2. 任务变化下的技能效用：历史评估与恢复评估的描述性汇总。面板 A 报告总体结果；面板 B 区分表示、实例和需求变化。每种方法均与相同变体上的无技能基线配对。得分及变体内差值采用表 1 的尺度。')]
font_dir=Path.home()/'.cache/babeldoc/fonts'
css="@font-face {font-family: repair; src: url(SourceHanSerifCN-Regular.ttf);} @font-face {font-family: repair; font-weight: bold; src: url(SourceHanSerifCN-Bold.ttf);} * {font-family: repair; font-size: 9pt; line-height: 1.05; margin: 0; padding: 0;}"
import html
for pi,box,translation in translation_repairs:
 page=doc[pi];rect=fitz.Rect(box);page.add_redact_annot(rect,fill=(1,1,1));page.apply_redactions(images=0,graphics=0)
 rendered=html.escape(translation)
 if translation.startswith('3. '):rendered='<div style="text-align:center"><b>'+rendered+'</b></div>'
 if translation.startswith('源任务上的提升'):head,tail=rendered.split('。',1);rendered='<b>'+head+'。</b>'+tail
 spare,scale=page.insert_htmlbox(rect,rendered,css=css,archive=fitz.Archive(str(font_dir)),scale_low=1)
 assert spare>=0 and scale==1,(pi,spare,scale)
for cp,dp in zip(clean,doc):assert canon(cp.get_text())==canon(dp.get_text(clip=cp.rect))
doc.subset_fonts()
for r in ann:
 page=doc[r['page']-1]
 a=page.add_highlight_annot([fitz.Rect(q).quad for q in r['rects']]);a.set_colors(stroke=(1,.4,.4));a.set_opacity(.35);a.set_info(title='Codex · 原版差异 · 2026-09-22',content=r['comment']);a.update()
out=root/'output/pdf/main-bilingual-en-zh.pdf';doc.save(out,garbage=4,deflate=True);doc.close();doc=fitz.open(out)
assert sum(len(list(p.annots() or [])) for p in doc)==len(ann)==33
sheet=Image.new('RGB',(1244,421*math.ceil(len(doc)/2)),'white')
for i,p in enumerate(doc):
 pix=p.get_pixmap(matrix=fitz.Matrix(1.1,1.1));pix.save(qa/f'dual-{i+1}.png');im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((602,390));tile=Image.new('RGB',(622,421),'#eee');tile.paste(im,(10,22));ImageDraw.Draw(tile).text((10,5),f'Page {i+1}',fill='black');sheet.paste(tile,((i%2)*622,(i//2)*421))
sheet.save(qa/'contact.png')
# Render clean red comparison as well.
high=fitz.open(root/'output/pdf/main-revision-highlighted.pdf')
for i in [0,2,3,7]:high[i].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(qa/f'highlight-{i+1}.png')
name='最新双语-ICASSP2027格式-红色对比-20260922.pdf';target=root/'tmp/pdfs/zotero-final-comparison-20260922'/name;shutil.copy2(out,target)
files={}
for name in ['main.pdf','main-revision-highlighted.pdf','main-bilingual-en-zh.pdf','main-overleaf-original-20260921.pdf']:
 p=root/'output/pdf'/name;d=fitz.open(p);files[name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pages':len(d),'annotations':sum(len(list(p.annots() or [])) for p in d)}
record={'baseline_commit':'121a6182b','translation':{'plugin':'Zotero PDF2zh 4.1.7','engine':'pdf2zh_next','service':'siliconflowfree','task_id':'64da91a5-0465-4dcd-989a-683162b35700','mode':'English left / Chinese right','result':result},'files':files,'validation':{'english_text_identical_to_clean':True,'red_highlights':33,'english_side_only':True,'clean_pages':8,'undefined_references':0,'overfull_boxes':0,'underfull_boxes':4},'translation_repairs':[{'page':p+1,'rect':list(box),'chinese':txt} for p,box,txt in translation_repairs],'zotero':{'status':'pending import','import_path':str(target)}}
(root/'paper/audits/zotero-bilingual-20260921/icassp2027-format-20260922.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(files,indent=2))
