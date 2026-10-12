"""Generate Chinese captions and headers without changing numeric table data."""
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]

table_translations = {
'Frozen scene- and mode-specific information weights. OFF disables the observer and every auxiliary branch.':'固定的场景与模式信息权重。OFF 关闭观测器及全部辅助分支。',
'Position ATE RMSE (m) after rigid alignment without scale. Bold denotes the minimum in each row; very small differences are not interpreted as significant gains.':'不带尺度的刚体对齐后位置 ATE RMSE（m）。加粗表示每行最小值；极小差异不解释为显著收益。',
'Mean per-sequence relative ATE reduction (\\%). Positive is improvement; each sequence receives equal weight.':'逐序列相对 ATE 降幅的平均值（\\%）。正值表示改善，各序列权重相同。',
'Relative error reductions of GVL against OFF in Machine Hall (\\%). Tail is position RMSE over the final 10\\% of matched support; max is the maximum aligned position error.':'Machine Hall 中 GVL 相对 OFF 的误差降幅（\\%）。末段为匹配评估集合最后 10\\% 的位置 RMSE；最大值为最大对齐位置误差。',
'Frames with actually applied auxiliary branches in GVL. Counts can differ because each branch has its own validity conditions.':'GVL 中各辅助分支实际施加的帧数。各分支有效性条件不同，因此计数可能不同。',
'Median per-sequence increases over OFF (\\%). Camera P95 measures only the camera API; full-run CPU and wall time include the complete replay. One serial paired measurement per sequence and mode.':'逐序列相对 OFF 增幅的中位数（\\%）。相机 P95 仅测量相机 API；全运行 CPU 和墙钟时间包含完整回放。每个序列、模式进行一次串行配对测量。',
'Scene & Mode':'场景 & 模式',
'Sequence &':'序列 &',
'Mode & MH (4) & Vicon (6) & All (10) & Lower ATE':'模式 & MH（4） & Vicon（6） & 全部（10） & ATE 降低',
'Tail & Max':'末段 & 最大值',
'Mode & Camera P95 & CPU time & Wall time & Peak RSS':'模式 & 相机 P95 & CPU 时间 & 墙钟时间 & 峰值 RSS'
}
(root / 'tables/zh').mkdir(exist_ok=True)
for path in (root / 'tables').glob('*.tex'):
    content = path.read_text()
    # Chinese remains single-column, regardless of the English float layout.
    content = content.replace(r'\begin{table*}[t]', r'\begin{table}[tb]')
    content = content.replace(r'\end{table*}', r'\end{table}')
    content = content.replace(r"\begin{adjustbox}{max width=\columnwidth}" + "\n", "")
    content = content.replace(r"\end{adjustbox}" + "\n", "")
    for old,new in table_translations.items():
        content = content.replace(old,new)
    assert re.findall(r'(?<![A-Za-z])[-+]?\d+\.\d+',content) == re.findall(r'(?<![A-Za-z])[-+]?\d+\.\d+',path.read_text())
    (root / 'tables/zh' / path.name).write_text(content)
