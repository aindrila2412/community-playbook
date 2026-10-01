#!/usr/bin/env python3
"""Attendance report for an event from a CSV (SAMPLE DATA ONLY by default).

Usage:
    python scripts/event_report.py
    python scripts/event_report.py --input data/attendance_sample.csv --outdir output --event-length 90
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REQUIRED = ["registrant_id", "level_group", "referral_source", "registered_on", "attended",
            "minutes_attended", "member_type", "feedback_rating"]


def rate_by(df: pd.DataFrame, col: str) -> pd.DataFrame:
    g = df.groupby(col).agg(registered=("registrant_id", "count"), attended=("attended_flag", "sum"))
    g["attendance_rate_pct"] = g["attended"] / g["registered"] * 100
    return g.sort_values("registered", ascending=False).reset_index()


def md(df: pd.DataFrame) -> str:
    head = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    rows = ["| " + " | ".join(f"{v:.1f}" if isinstance(v, float) else str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join([head, sep, *rows])


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", default="data/attendance_sample.csv")
    p.add_argument("--outdir", default="output")
    p.add_argument("--event-length", type=int, default=90, help="Event length in minutes")
    a = p.parse_args()

    df = pd.read_csv(a.input)
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise SystemExit(f"Missing columns: {sorted(missing)}")
    df["attended_flag"] = df["attended"].str.strip().str.lower().eq("yes")
    reg, att = len(df), int(df["attended_flag"].sum())
    attendees = df[df["attended_flag"]]
    stayed = (attendees["minutes_attended"] >= 0.5 * a.event_length).mean() * 100 if att else 0.0
    rated = attendees["feedback_rating"].dropna()

    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)

    by_src = rate_by(df, "referral_source")
    by_lvl = rate_by(df, "level_group")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].bar(by_src["referral_source"], by_src["registered"], label="Registered", color="#BBBBBB")
    axes[0].bar(by_src["referral_source"], by_src["attended"], label="Attended", color="#4C78A8")
    axes[0].set_title("By referral source")
    axes[0].tick_params(axis="x", rotation=25)
    axes[0].legend(fontsize=8)
    if len(rated):
        counts = rated.astype(int).value_counts().sort_index()
        axes[1].bar(counts.index.astype(str), counts.values, color="#54A24B")
    axes[1].set_title("Feedback ratings (1-5)")
    fig.suptitle("Event attendance - SAMPLE (FICTIONAL) DATA")
    fig.tight_layout()
    fig.savefig(out / "event_summary.png", dpi=150)
    plt.close(fig)

    lines = [
        "# Event attendance report",
        "",
        "> **Sample data only.** Fictional registrations; not a real event.",
        "",
        f"- Source: `{a.input}`",
        f"- Registered: {reg}",
        f"- Attended: {att} ({att / reg * 100:.1f}%)",
        f"- No-shows: {reg - att}",
        f"- Stayed at least half the event ({a.event_length // 2}+ min): {stayed:.1f}% of attendees",
        f"- Feedback responses: {len(rated)} ({len(rated) / att * 100:.1f}% of attendees)" if att else "- Feedback responses: 0",
        f"- Mean feedback rating: {rated.mean():.2f}" if len(rated) else "- Mean feedback rating: n/a",
        "",
        "![Summary](event_summary.png)",
        "",
        "## Attendance by referral source",
        "",
        md(by_src),
        "",
        "## Attendance by level group",
        "",
        md(by_lvl),
        "",
        "## New versus returning",
        "",
        md(rate_by(df, "member_type")),
        "",
        "## Caveats",
        "",
        "- Feedback comes only from attendees who chose to respond, so it may not be representative.",
        "- Small groups make percentages unstable.",
        "",
    ]
    (out / "event_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Registered {reg}, attended {att} -> {out}/event_report.md, {out}/event_summary.png")


if __name__ == "__main__":
    main()
