# Community Playbook

A personal, reusable set of templates and two small Python scripts for running an online learning community: strategy and onboarding, a content calendar, a code of conduct with moderation guidelines, an engagement-metrics report, and an event playbook with a post-event attendance report.

> **Personal template project. Sample data only.**
> "Example Learners Club" is an invented community. All names, dates, amounts, and figures are **fictional** and were generated for demonstration. Nothing here describes a real community, client, or employer, and no real results are claimed.

## Purpose

To practise and share a clear, humane structure for community management: welcome people well, keep the space safe, plan content and events, and measure health with metrics that lead to action.

## Structure

```text
community-playbook/
├── README.md
├── LICENSE
├── .gitignore
├── .markdownlint.json
├── requirements.txt
├── .github/workflows/ci.yml
├── docs/
│   ├── community-strategy-and-onboarding.md
│   ├── code-of-conduct-and-moderation.md
│   └── engagement-metrics.md
├── events/event-playbook.md
├── templates/
│   ├── content-calendar-template.csv
│   ├── moderation-log-template.csv
│   ├── event-planning-checklist.md
│   ├── speaker-volunteer-tracker-template.csv
│   ├── event-comms-calendar-template.csv
│   ├── event-budget-template.csv
│   └── post-event-report-template.md
├── data/                                   # FICTIONAL samples
│   ├── content_calendar_sample.csv
│   ├── engagement_sample.csv
│   ├── attendance_sample.csv
│   ├── speaker_volunteer_sample.csv
│   ├── event_comms_sample.csv
│   └── event_budget_sample.csv
├── scripts/
│   ├── engagement_report.py                # weekly engagement metrics + chart
│   └── event_report.py                     # attendance report + chart
└── output/                                 # generated from the sample data
```

## How to use it

1. Read [strategy and onboarding](docs/community-strategy-and-onboarding.md) and adapt it to your community.
2. Adopt or adapt the [code of conduct and moderation guide](docs/code-of-conduct-and-moderation.md).
3. Plan content with the content calendar template.
4. Plan events with the [event playbook](events/event-playbook.md) and the templates.
5. Run the reports:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/engagement_report.py
python scripts/event_report.py
```

Both scripts accept `--input` and `--outdir`; the default input is the fictional sample.

## Limitations

- Templates are starting points; adapt them to your platform, culture, and local law.
- The code of conduct is not legal advice.
- Sample data is random and is only for checking that the scripts work.

## Licence

MIT. See [LICENSE](LICENSE).
