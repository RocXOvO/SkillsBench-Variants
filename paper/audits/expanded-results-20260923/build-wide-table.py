import json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
z=json.loads((Path(__file__).parent/'statistics.json').read_text())
a=[r'\end{multicols}',r'\noindent\begin{minipage}{\textwidth}',r'\centering',r'\small',r'\setlength{\tabcolsep}{8pt}',r'\renewcommand{\arraystretch}{1.08}',r'\begin{tabular}{llrrrrrrrrr}',r'\toprule',r'\textbf{Method} & \textbf{Evaluation} & $N$ & \textbf{No skill} & \textbf{Skill} & $\Delta$ & \textbf{I} & \textbf{R} & \textbf{T} & $G$ & $L$ \\',r'\midrule']
for method in ['SkillEvolver','SPARK','CoEvoSkills']:
 for j,(label,q) in enumerate(z[method]['rows'].items()):
  if label == 'Variants: all': continue
  a.append(f"{method if j==0 else ''} & {label} & {q['n']} & {q['baseline']:.2f} & {q['skill']:.2f} & ${q['delta']:+.2f}$ & {q['improved']} & {q['regressed']} & {q['tied']} & {q['gain_mass']:.2f} & {q['loss_mass']:.2f} "+r'\\')
 a.append(r'\midrule')
a += [r'\multicolumn{11}{l}{\textbf{Baseline-conditioned variant outcomes}}\\',r'\textbf{Method} & \multicolumn{2}{c}{\textbf{Baseline zero}} & \multicolumn{2}{c}{\textbf{Zero to positive}} & \multicolumn{2}{c}{\textbf{Zero to full}} & \multicolumn{2}{c}{\textbf{Baseline full}} & \multicolumn{2}{c}{\textbf{Full to lower}}\\',r'\midrule']
for method in ['SkillEvolver','SPARK','CoEvoSkills']:
 q=z[method]['rows']['Variants: all']; a.append(method+' & '+' & '.join(r'\multicolumn{2}{c}{'+str(q[k])+'}' for k in ['baseline_zero','zero_to_positive','zero_to_full','baseline_full','full_to_lower'])+r'\\')
a += [r'\bottomrule',r'\end{tabular}',r'\captionof{table}{Completed-skill utility on source tasks and controlled variants. Rewards, paired gains $\Delta$, positive contributions $G$, and negative contributions $L$ use a 0--100 scale, with $\Delta=G-L$ before rounding. I/R/T counts improved, regressed, and tied tasks. P1: input representation; P2: task instance; P3: coupled requirements. Variant rows describe the complete historical and recovery record, pairing each skill result with its same-variant no-skill baseline. The lower panel counts transitions from zero or full baseline reward; each method also has ten intermediate-baseline variants.}',r'\label{tab:skillsbench-six-runs}',r'\label{tab:variant-transfer}',r'\end{minipage}',r'\par\vspace{6pt}',r'\begin{multicols}{2}']
(R/'paper/maintext-20260921/skillsbench-variant-table.tex').write_text('\n'.join(a)+'\n')
