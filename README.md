# Community Playbook

A set of templates and two small Python scripts for running an online learning community. I made it to practise
thinking through community management: welcoming people, keeping the space safe, planning content and events, and
picking metrics that actually lead to something you can do.

The community in it, "Example Learners Club", is made up. All the names, dates, amounts and numbers are fictional and
were generated just to show the scripts working. It doesn't describe a real community, client or employer.

## What's in it

- `docs/` has the strategy and onboarding notes, a code of conduct with a moderation guide, and a note on engagement
  metrics.
- `events/event-playbook.md` covers planning an event from start to finish.
- `templates/` has the content calendar, moderation log, event checklist, speaker and volunteer tracker, comms
  calendar, budget and post-event report templates.
- `data/` is the fictional sample data, and `output/` is what the scripts produce from it.

## Running the scripts

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/engagement_report.py
python scripts/event_report.py
```

The first makes a weekly engagement report and chart. The second makes an attendance report and chart. Both take
`--input` and `--outdir`, and use the fictional sample by default.

## Honest notes

The templates are starting points, so you'd need to adapt them to your own platform and culture. The code of conduct is
not legal advice. The sample data is random, so only use it to check the scripts run. I'd like to add a template for
handling a moderation appeal next, since that's the part I find hardest to word well.

## Licence

MIT, see [LICENSE](LICENSE).
