# Engagement Metrics (TEMPLATE)

> Definitions and a worked example on **fictional sample data**. The numbers in `output/` come from generated sample data and say nothing about any real community.

## Principles

- Measure what you will act on. Fewer, clearer metrics beat dashboards.
- Pair counts with context; small communities have noisy numbers.
- Watch health as well as growth: sentiment, response time, and moderation load.

## Suggested metrics

| Metric | Definition | Why it matters |
|---|---|---|
| New members | Joins in the period | Growth |
| Active members | Members with at least one post, reply, or reaction in the period | Participation |
| Active rate | Active members divided by total members | Health, not just size |
| Posts and replies per active member | Contribution depth | Engagement depth |
| Reply rate | Threads with a reply divided by threads | Responsiveness |
| Median time to first reply | Thread created to first reply | New-member experience |
| Member retention (4 weeks) | New members still active 4 weeks later | Onboarding quality |
| Moderation actions | Count by level | Community health and moderator load |

## Running the sample script

```bash
pip install -r requirements.txt
python scripts/engagement_report.py
```

Input: [`data/engagement_sample.csv`](../data/engagement_sample.csv) (one row per week, fictional). Output: `output/engagement_report.md` and `output/engagement_trend.png`.

## Interpreting results

- Use the trend, not a single week.
- Investigate big changes against known events (for example a session or a holiday).
- Report limitations: sample size, how "active" is defined, and missing data.
