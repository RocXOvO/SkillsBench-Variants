from pathlib import Path
import fitz,json,hashlib,shutil,math,unicodedata
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[3];qa=root/'tmp/pdfs/icassp-flow-fix/dual';qa.mkdir(parents=True,exist_ok=True)
result=json.loads((root/'tmp/pdfs/icassp-flow-fix/translation-result.json').read_text())
p=next(Path(x) for x in result['filePaths'] if 'LR_dual' in x)
doc=fitz.open(p);clean=fitz.open(root/'output/pdf/main.pdf');assert len(doc)==len(clean)==8
# Repair translation-only fragments found during visual QA; English source is untouched.
translation_repairs = [
 (1, (927,354,1171,369), '3.2. 源任务收益在重复运行中保持', True, 9),
 (1, (679,483,911,515), '2. 效果归因：哪些反馈、修订、选择、执行和测量机制产生了观察到的收益？', False, 8.5),
 (2, (666,374,910,389), '3.4. 演化后的技能保留了什么', True, 9),
 (3, (804,288,932,341), '12/24 个任务在至少一种冻结条件下改变成功状态；所选结果的保留率：SkillRevise 为 47.1%，SkillHone 为 55.0%。', False, 8.3),
 (4, (666,235,1172,262), '图2. 生命周期归因设计及当前证据覆盖。上部定位各项干预，下部记录各方法的覆盖情况。已填单元格并不表示证据强度相同；缺失单元格界定了跨方法结论的边界。', False, 8.6),
 (5, (666,463,921,490), '这套审计并非从“安全”到“不安全”的单一阶梯。各步骤回答独立问题，并对应不同的结论边界。', False, 8.5),
 (5, (927,660,1172,675), '7.2. 智能体改进的评估与归因', True, 9),
 (5, (927,677,1172,704), '智能体评估日益关注过程质量、序贯适应、验证器可靠性和反事实行为。反事实轨迹审计衡量给定技能如何改变智能体的执行轨迹 [15]。', False, 8.2),
]
fontdir=Path('/Users/duchongyang/.cache/babeldoc/fonts')
css="""@font-face {font-family: zh; src: url(SourceHanSerifCN-Regular.ttf);}
@font-face {font-family: zh; src: url(SourceHanSerifCN-Bold.ttf); font-weight: bold;}
* {margin:0;padding:0;} body {font-family:zh;line-height:1.12;}"""
for pi, box, text, bold, size in translation_repairs:
 page=doc[pi];rect=fitz.Rect(box)
 page.add_redact_annot(rect,fill=(1,1,1));page.apply_redactions(images=0,graphics=0)
 html=f'<div style="font-size:{size}pt;font-weight:{"bold" if bold else "normal"}">{text}</div>'
 spare,scale=page.insert_htmlbox(rect,html,css=css,archive=fitz.Archive(str(fontdir)),scale_low=0.95)
 assert spare>=0,(pi,text,spare)
doc.subset_fonts()
ann=json.loads((root/'paper/audits/variant-maintext-20260921/original-comparison-highlights-20260922.json').read_text())['annotations']
canon=lambda s:''.join(c.lower() for c in unicodedata.normalize('NFKD',s) if c.isalnum())
for i,(cp,dp) in enumerate(zip(clean,doc)):
 assert abs(dp.rect.width-2*cp.rect.width)<1
 assert canon(cp.get_text())==canon(dp.get_text(clip=cp.rect)),i
for r in ann:
 page=doc[r['page']-1]
 a=page.add_highlight_annot([fitz.Rect(q).quad for q in r['rects']]);a.set_colors(stroke=(1,.4,.4));a.set_opacity(.35);a.set_info(title='Codex · 原版差异 · 2026-09-22',content=r['comment']);a.update()
out=root/'output/pdf/main-bilingual-en-zh.pdf';doc.save(out,garbage=4,deflate=True);doc.close();doc=fitz.open(out)
assert sum(len(list(p.annots() or [])) for p in doc)==len(ann)
sheet=Image.new('RGB',(1244,421*math.ceil(len(doc)/2)),'white')
for i,p in enumerate(doc):
 pix=p.get_pixmap(matrix=fitz.Matrix(1.1,1.1));pix.save(qa/f'dual-{i+1}.png');im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((602,390));tile=Image.new('RGB',(622,421),'#eee');tile.paste(im,(10,22));ImageDraw.Draw(tile).text((10,5),f'Page {i+1}',fill='black');sheet.paste(tile,((i%2)*622,(i//2)*421))
sheet.save(qa/'contact.png')
# Render clean red comparison as well.
high=fitz.open(root/'output/pdf/main-revision-highlighted.pdf')
for i in [0,1,2,3,4,5,6,7]:high[i].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(qa/f'highlight-{i+1}.png')
name='最新双语-ICASSP表格修复-红色对比-20260922.pdf';target=root/'tmp/pdfs/zotero-final-comparison-20260922'/name;shutil.copy2(out,target)
files={}
for name in ['main.pdf','main-revision-highlighted.pdf','main-bilingual-en-zh.pdf','main-overleaf-original-20260921.pdf']:
 p=root/'output/pdf'/name;d=fitz.open(p);files[name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pages':len(d),'annotations':sum(len(list(p.annots() or [])) for p in d)}
record={'baseline_commit':'121a6182b','translation':{'plugin':'Zotero PDF2zh 4.1.7','engine':'pdf2zh_next','service':'siliconflowfree','task_id':'e918e191-f669-43b9-8f6a-f6459358dd67','mode':'English left / Chinese right','result':result,'manual_translation_repairs':[{'page':p+1,'rect':b,'text':t} for p,b,t,_,_ in translation_repairs]},'files':files,'validation':{'english_text_identical_to_clean':True,'red_highlights':len(ann),'english_side_only':True,'clean_pages':8,'undefined_references':0,'overfull_boxes':0,'underfull_boxes':0},'zotero':{'status':'pending import','import_path':str(target)}}
(root/'paper/audits/zotero-bilingual-20260921/icassp-flow-fix-20260922.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(files,indent=2))
