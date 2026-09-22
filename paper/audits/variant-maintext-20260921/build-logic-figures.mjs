import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
import { finalizePresentation, resolvePresentationFont } from '/Users/duchongyang/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations/container_tools/artifact_tool_utils.mjs';
const ROOT='/Users/duchongyang/Documents/ICLR';
const TMP=path.join(ROOT,'tmp/ppt-logic-20260922');
const SKILL='/Users/duchongyang/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations';
const family=resolvePresentationFont({fontFamily:'Arial'});
const p=Presentation.create({slideSize:{width:1200,height:400}});
const C={ink:'#233446', muted:'#536579', line:'#728394', blue:'#E5EFF8', blueEdge:'#5E83A5', purple:'#EEE8F7', purpleEdge:'#9276AD', green:'#E5F1E9', greenEdge:'#54836A', amber:'#FBF0DC', amberEdge:'#B68B48', red:'#F6E5E5', redEdge:'#B67575', gray:'#F0F2F4'};
function box(s,x,y,w,h,fill,edge){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:edge,width:1.4},borderRadius:7});}
function txt(s,text,x,y,w,h,size=22,bold=false,color=C.ink,align='left'){const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=text;t.text.style={typeface:family,fontSize:size,bold,color,alignment:align,verticalAlignment:'middle',autoFit:'none',insets:{left:0,right:0,top:0,bottom:0}};return t;}
function arrow(s,a,b,color=C.line,from='right',to='left',kind='straight'){return s.shapes.connect(a,b,{fromSide:from,toSide:to,kind,line:{fill:color,width:2},tail:{type:'triangle',width:'sm',length:'sm'}});}
const a=p.slides.add();a.background.fill='#FFFFFF';
txt(a,'Frozen-skill evaluation on controlled task variants',20,8,1160,33,25,true);
txt(a,'Source task',20,55,150,30,21,true);txt(a,'Retained artifact',217,55,171,30,21,true);txt(a,'Task changes',447,55,290,30,21,true);txt(a,'Paired evaluation of each variant',788,55,390,30,21,true);
const source=box(a,20,153,153,110,C.gray,C.line);txt(a,'Generate or\nevolve a skill',29,165,135,85,23,true,C.ink,'center');
const frozen=box(a,220,153,177,110,C.blue,C.blueEdge);txt(a,'Freeze the\nfinal skill',230,165,157,85,23,true,C.ink,'center');arrow(a,source,frozen);
const rows=[['P1','Input representation',C.purple,C.purpleEdge,103],['P2','Task instance',C.amber,C.amberEdge,188],['P3','Coupled requirements',C.green,C.greenEdge,273]];
const variants=[];for(const [lab,body,bg,ed,y] of rows){const q=box(a,447,y,283,66,bg,ed);txt(a,lab,460,y+10,40,45,23,true);txt(a,body,510,y+8,208,49,21);variants.push(q);arrow(a,frozen,q,C.line,'right','left','elbow');}
const evalBox=box(a,785,103,391,236,'#FFFFFF',C.line);
const yes=box(a,800,117,173,67,C.blue,C.blueEdge);txt(a,'With frozen skill',810,126,153,48,21,true,C.ink,'center');
const no=box(a,989,117,173,67,C.gray,C.line);txt(a,'Without skill',999,126,153,48,21,true,C.ink,'center');
txt(a,'Same variant and verifier',804,194,355,31,21,false,C.muted,'center');
txt(a,'Paired reward difference',805,242,355,33,23,true,C.ink,'center');
txt(a,'Scope of skill utility',805,290,355,33,23,true,C.blueEdge,'center');
for(const q of variants)arrow(a,q,evalBox,C.line,'right','left','elbow');
txt(a,'The skill remains fixed across P1–P3. Execution adapts to the changed task.',20,356,1160,30,21,false,C.muted);
a.speakerNotes.textFrame.setText('Original editable figure for Are Self-Evolving Agent Skills Learning Skills? Protocol basis: paper/maintext-20260921/skillsbench-variants.tex and full-variant-records-20260922 audit. Paired difference is final skill versus no skill on the same variant, not pre-evolution versus post-evolution. Workflow figure design reference only: Wang et al. (2026), SAGE, Figure 1, https://aclanthology.org/2026.acl-long.69.pdf. No image or diagram copied.');
const b=p.slides.add();b.background.fill='#FFFFFF';
txt(b,'Reusable decisions in the inspected skill artifacts and execution traces',20,8,1160,33,25,true);
txt(b,'Skill content',20,60,248,30,21,true);txt(b,'Execution on a changed task',351,60,471,30,21,true);txt(b,'Observed outcome',908,60,276,30,21,true);
const rules=box(b,20,103,255,132,C.blue,C.blueEdge);txt(b,'Diagnostic rules',33,115,229,34,22,true);txt(b,'When to revise',33,157,229,31,21);txt(b,'Output constraints',33,196,229,31,22,true);
const adapt=box(b,349,103,475,132,C.green,C.greenEdge);txt(b,'Adapt inputs and solution construction',364,113,444,36,23,true);txt(b,'Keep the diagnostic rule',364,156,440,28,22);txt(b,'Preserve and check task constraints',364,193,440,28,22);
const success=box(b,905,103,272,132,C.green,C.greenEdge);txt(b,'Successful reuse',920,128,242,36,24,true,C.greenEdge,'center');txt(b,'Rules remain effective\nafter the task changes',920,171,242,51,21,false,C.ink,'center');
arrow(b,rules,adapt,C.greenEdge);arrow(b,adapt,success,C.greenEdge);
const procedure=box(b,20,266,255,86,C.gray,C.line);txt(b,'Procedure carried over',33,279,229,59,22,true,C.ink,'center');
const omission=box(b,349,266,475,86,C.red,C.redEdge);txt(b,'Required decision or constraint missed',364,279,444,59,23,true,C.ink,'center');
const failure=box(b,905,266,272,86,C.red,C.redEdge);txt(b,'Verification failure',920,279,242,59,23,true,C.redEdge,'center');
arrow(b,procedure,omission,C.redEdge);arrow(b,omission,failure,C.redEdge);
txt(b,'Interpretation of inspected cases: the reusable unit includes a decision and its correctness conditions.',20,366,1160,25,20,false,C.muted);
b.speakerNotes.textFrame.setText('Conceptual synthesis of the inspected SkillEvolver, SPARK, and CoEvoSkills artifact and execution cases in paper/audits/variant-maintext-20260921/skill-reuse-writing-revision-20260922.md. This is an interpretation of observed cases, not a causal ablation, learned mechanism measurement, or universal description of any method. No method identity is assigned to a pathway. Visual reference only: SAGE Figure 1, https://aclanthology.org/2026.acl-long.69.pdf. Original editable shapes and connectors.');
const candidate=path.join(TMP,'candidate.pptx');await (await PresentationFile.exportPptx(p)).save(candidate);
for(let i=0;i<2;i++){const slide=p.slides.getItem(i);const image=await p.export({slide,format:'png',scale:2});await fs.writeFile(path.join(TMP,`slide-${i+1}.png`),new Uint8Array(await image.arrayBuffer()));const layout=await slide.export({format:'layout'});await fs.writeFile(path.join(TMP,`slide-${i+1}.layout.json`),await layout.text());}
await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath:path.join(ROOT,'output/pptx/skill-transfer-logic-20260922-r3.pptx'),pythonExecutable:'/Users/duchongyang/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','11430000,3810000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:2,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:[family]},verifyArtifactToolImport:true,receiptPath:path.join(TMP,'validation-r3.json')});
console.log('Created two-slide editable logic figures.');
