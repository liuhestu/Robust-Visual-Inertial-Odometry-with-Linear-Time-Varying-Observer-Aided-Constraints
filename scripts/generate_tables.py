#!/usr/bin/env python3
"""Regenerate manuscript tables from the frozen EuRoC JSON snapshot."""
import json
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tables"
MODES = ["OFF", "G", "V", "L", "GVL"]
SEQS = ["MH_01_easy", "MH_02_easy", "MH_03_medium", "MH_05_difficult",
        "V1_01_easy", "V1_02_medium", "V1_03_difficult", "V2_01_easy",
        "V2_02_medium", "V2_03_difficult"]

def read(name):
    return json.loads((ROOT / "data" / name).read_text())

def table(name, caption, label, cols, header, rows):
    environment = "table*" if name == "ate.tex" else "table"
    placement = "t" if environment == "table*" else "tb"
    text = "\\begin{" + environment + "}[" + placement + "]\n\\caption{" + caption + "}\\label{" + label + "}\n"
    text += "\\centering\\small\n"
    if environment == "table":
        text += "\\begin{adjustbox}{max width=\\columnwidth}\n"
    text += "\\begin{tabular}{" + cols + "}\n\\toprule\n"
    text += header + " \\\\\n\\midrule\n"
    text += "\n".join(" & ".join(row) + " \\\\" for row in rows)
    text += "\n\\bottomrule\n\\end{tabular}\n"
    if environment == "table":
        text += "\\end{adjustbox}\n"
    text += "\\end{" + environment + "}\n"
    (OUT / name).write_text(text)

def main():
    OUT.mkdir(exist_ok=True)
    runs = read("results.json")
    metrics = read("metrics.json")
    summary = read("analysis_summary.json")
    protocol = read("protocol.json")
    assert len(runs) == 50 and len(metrics) == 50
    run = {(x["sequence"], x["mode"]): x for x in runs}
    met = {(x["sequence"], x["mode"]): x for x in metrics}
    assert len(run) == 50 and len(met) == 50
    assert all(x["status"] == "VALID_FULL_MATCHED" and x["coverage"] == 1 for x in runs)
    for s in SEQS:
        base = run[s, "OFF"]["ate_rmse_m"]
        for mode in MODES:
            x = run[s, mode]
            assert abs(100 * (x["ate_rmse_m"] / base - 1) - x["relative_off_percent"]) < 1e-9
            assert abs(met[s, mode]["ate_rmse_m"] - x["ate_rmse_m"]) < 1e-12

    rows = []
    for scene in ["MH", "Vicon"]:
        for mode in MODES[1:]:
            g, v, l = protocol["profiles"][scene][mode]
            rows.append([scene, mode, str(g) if g else "--", str(v) if v else "--", str(l) if l else "--"])
    table("weights.tex", "Frozen scene- and mode-specific information weights. OFF disables the observer and every auxiliary branch.",
          "tab:weights", "llrrr", r"Scene & Mode & $\alpha_G$ & $\alpha_V$ & $\alpha_L$", rows)

    rows = []
    for s in SEQS:
        vals = [run[s, mode]["ate_rmse_m"] for mode in MODES]
        best = min(vals)
        rows.append([s.split("_")[0] + "\\_" + s.split("_")[1]] +
                    ["\\textbf{" + f"{v:.6f}" + "}" if v == best else f"{v:.6f}" for v in vals])
    table("ate.tex", "Position ATE RMSE (m) after rigid alignment without scale. Bold denotes the minimum in each row; very small differences are not interpreted as significant gains.",
          "tab:ate", "lrrrrr", "Sequence & OFF & G & V & L & GVL", rows)

    rows = []
    for mode in MODES[1:]:
        mh = [run[s, mode] for s in SEQS[:4]]
        vi = [run[s, mode] for s in SEQS[4:]]
        both = mh + vi
        rows.append([mode, f"{-mean(x['relative_off_percent'] for x in mh):.3f}",
                     f"{-mean(x['relative_off_percent'] for x in vi):.3f}",
                     f"{-mean(x['relative_off_percent'] for x in both):.3f}",
                     f"{sum(x['relative_off_percent'] < 0 for x in both)}/10"])
    table("summary.tex", "Mean per-sequence relative ATE reduction (\\%). Positive is improvement; each sequence receives equal weight.",
          "tab:summary", "lrrrr", "Mode & MH (4) & Vicon (6) & All (10) & Lower ATE", rows)

    rows = []
    for s in SEQS[:4]:
        a, b = met[s, "OFF"], met[s, "GVL"]
        keys = ["ate_rmse_m", "rpe_translation_1s_m", "rpe_translation_5s_m", "support_last10pct_rmse_m", "position_max_m"]
        rows.append([s.split("_")[0] + "\\_" + s.split("_")[1]] + [f"{100*(1-b[k]/a[k]):.2f}" for k in keys])
    table("mh_metrics.tex", "Relative error reductions of GVL against OFF in Machine Hall (\\%). Tail is position RMSE over the final 10\\% of matched support; max is the maximum aligned position error.",
          "tab:mhmetrics", "lrrrrr", r"Sequence & ATE & RPE-T 1 s & RPE-T 5 s & Tail & Max", rows)

    rows = []
    for s in SEQS:
        audit = run[s, "GVL"]["audit"]
        rows.append([s.split("_")[0] + "\\_" + s.split("_")[1]] + [str(audit[f"actual_{k}"]) for k in ["G", "V", "L"]])
    table("updates.tex", "Frames with actually applied auxiliary branches in GVL. Counts can differ because each branch has its own validity conditions.",
          "tab:updates", "lrrr", "Sequence & G & V & L", rows)

    rows = []
    for x in summary["paired_cost"]:
        d = x["median_percent"]
        rows.append([x["mode"]] + [f"+{d[k]:.2f}" for k in
                    ["camera_api_p95_ms", "full_cpu_s", "full_wall_s", "peak_rss_kb"]])
    table("cost.tex", "Median per-sequence increases over OFF (\\%). Camera P95 measures only the camera API; full-run CPU and wall time include the complete replay. One serial paired measurement per sequence and mode.",
          "tab:cost", "lrrrr", "Mode & Camera P95 & CPU time & Wall time & Peak RSS", rows)
    print("Validated 50 cases; regenerated 6 manuscript tables.")

if __name__ == "__main__":
    main()
