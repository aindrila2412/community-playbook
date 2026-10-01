#!/usr/bin/env python3
"""Weekly community engagement report from a CSV (SAMPLE DATA ONLY by default).

Usage:
    python scripts/engagement_report.py
    python scripts/engagement_report.py --input data/engagement_sample.csv --outdir output
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REQUIRED = [
    "week_start", "total_members", "new_members", "active_members", "posts_and_replies",
    "threads", "threads_with_reply", "median_hours_to_first_reply",
    "new_members_active_after_4w", "moderation_actions",
]


def compute(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["week_start"] = pd.to_datetime(df["week_start"])
    df["active_rate_pct"] = df["active_members"] / df["total_members"] * 100
    df["posts_per_active"] = df["posts_and_replies"] / df["active_members"]
    df["reply_rate_pct"] = df["threads_with_reply"] / df["threads"] * 100
    df["retention_4w_pct"] = df["new_members_active_after_4w"] / df["new_members"] * 100
    return df.sort_values("week_start")


def table(df: pd.DataFrame) -> str:
    head = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    body = ["| " + " | ".join(f"{v:.1f}" if isinstance(v, float) else str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join([head, sep, *body])


def chart(df: pd.DataFrame, path: Path) -> None:
    fig, ax1 = plt.subplots(figsize=(9, 4.5))
    ax1.plot(df["week_start"], df["active_members"], marker="o", color="#4C78A8", label="Active members")
    ax1.bar(df["week_start"], df["new_members"], width=4, color="#F58518", alpha=0.6, label="New members")
    ax1.set_ylabel("Members")
    ax2 = ax1.twinx()
    ax2.plot(df["week_start"], df["reply_rate_pct"], color="#54A24B", linestyle="--", label="Reply rate %")
    ax2.set_ylabel("Reply rate (%)")
    ax2.set_ylim(0, 100)
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8)
    ax1.set_title("Weekly engagement - SAMPLE (FICTIONAL) DATA")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def report(df: pd.DataFrame, source: str) -> str:
    last4, prev4 = df.tail(4), df.iloc[-8:-4]
    def m(d, c): return d[c].mean()
    def delta(c):
        return f"{m(last4, c):.1f} (previous 4 weeks: {m(prev4, c):.1f})" if len(prev4) == 4 else f"{m(last4, c):.1f}"
    ret = df["retention_4w_pct"].dropna()
    busiest = df.loc[df["new_members"].idxmax()]
    lines = [
        "# Engagement report",
        "",
        "> **Sample data only.** Generated fictional data; it does not describe any real community.",
        "",
        f"- Source: `{source}`",
        f"- Weeks covered: {len(df)} ({df['week_start'].min().date()} to {df['week_start'].max().date()})",
        f"- Total members at end: {int(df['total_members'].iloc[-1])}",
        f"- New members in period: {int(df['new_members'].sum())}",
        "",
        "## Last 4 weeks (average per week)",
        "",
        f"- Active members: {delta('active_members')}",
        f"- Active rate (%): {delta('active_rate_pct')}",
        f"- Posts and replies per active member: {delta('posts_per_active')}",
        f"- Reply rate (%): {delta('reply_rate_pct')}",
        f"- Median hours to first reply: {delta('median_hours_to_first_reply')}",
        f"- Moderation actions: {delta('moderation_actions')}",
        "",
        "## Whole period",
        "",
        f"- Mean 4-week retention of new members (%): {ret.mean():.1f} (weeks with data: {len(ret)})",
        f"- Week with most joins: {busiest['week_start'].date()} ({int(busiest['new_members'])} new)",
        f"- Total moderation actions: {int(df['moderation_actions'].sum())}",
        "",
        "![Trend](engagement_trend.png)",
        "",
        "## Weekly detail",
        "",
        table(df[["week_start", "new_members", "active_members", "active_rate_pct", "reply_rate_pct", "median_hours_to_first_reply"]].assign(week_start=df["week_start"].dt.date)),
        "",
        "## Caveats",
        "",
        "- Weekly numbers are noisy; look at trends and compare with known events.",
        "- \"Active\" is defined as any post, reply, or reaction; change the definition and the numbers change.",
        "- Early weeks have no 4-week retention value yet.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", default="data/engagement_sample.csv")
    p.add_argument("--outdir", default="output")
    a = p.parse_args()
    raw = pd.read_csv(a.input)
    missing = set(REQUIRED) - set(raw.columns)
    if missing:
        raise SystemExit(f"Missing columns: {sorted(missing)}")
    df = compute(raw)
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    chart(df, out / "engagement_trend.png")
    (out / "engagement_report.md").write_text(report(df, a.input), encoding="utf-8")
    print(f"Report for {len(df)} weeks -> {out}/engagement_report.md, {out}/engagement_trend.png")


if __name__ == "__main__":
    main()
