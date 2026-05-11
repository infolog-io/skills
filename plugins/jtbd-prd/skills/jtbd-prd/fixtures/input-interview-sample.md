---
source_id: interview-acme-2026-04-12
role: Senior Engineer
company: Acme Corp
date: 2026-04-12
interviewer: BL
---

<!--
LABELED JOBS (used by extractor tests, hidden in extractor input):
JOB-A: triage stale PRs on Monday morning
JOB-B: confirm reviewer has context before assigning
JOB-C: avoid being seen as the team bottleneck
JOB-D: keep shipping cadence around code freezes
JOB-E: recover from incident reviews without losing a day to writeups
-->

**Interviewer:** Walk me through a typical Monday morning.

**Customer:** Honestly, Mondays are the worst. I open Slack and immediately
see twelve pings from people waiting on my review. Half the time I don't
even know which PR they're talking about. By the time I've triaged them I've
lost ninety minutes and the team's already in standup.

**Interviewer:** What would make that better?

**Customer:** I don't know. Maybe just... see them all in one place? With
context. Right now it's like every PR is a cold start. I'm reading the diff,
the description, trying to remember what we even decided about this feature
in the design review. It's exhausting.

**Interviewer:** Has there ever been a Monday where this worked?

**Customer:** Yeah, when our team lead used to do triage for the whole team
before standup. She'd assign reviews and ping the right person. We stopped
doing that when she went on leave and never picked it back up.

**Interviewer:** Tell me about a recent PR review that went well.

**Customer:** Last Wednesday someone pinged me directly with "hey, you wrote
the auth middleware, can you look at this change to it?" That was great
because I had context already. I reviewed it in fifteen minutes. The bad
ones are when I get assigned to something I have no history with — I end up
spending an hour just figuring out what the change is supposed to do before
I can review it.

**Interviewer:** Who decides who reviews what?

**Customer:** Mostly the author. Sometimes they pick whoever's online,
sometimes they pick the person they like working with. It's pretty random.
The CODEOWNERS file is out of date — half the people in it left the company
last year. Nobody's updated it.

**Interviewer:** When a PR sits for too long, what happens?

**Customer:** It blocks everything downstream. Other people can't merge,
the engineer who wrote it gets nervous, they ping me in DM, then on Slack,
then they walk to my desk. By the time it merges they've spent more time
following up than writing the code.

**Interviewer:** Have you tried any tools for this?

**Customer:** We have a Slack bot that pings the assigned reviewer every
day. It's annoying — it pings even when the PR is waiting on the author for
changes. People mute it. So now nothing pings and we're back where we
started.

**Interviewer:** Tell me about code freezes.

**Customer:** Code freezes are brutal. The week before a freeze everyone
tries to merge everything. Reviews stack up. The senior engineers spend
that whole week as full-time reviewers. We don't ship our own work. After
the freeze we're a week behind and management asks why we missed our
sprint commitments.

**Interviewer:** Anything else?

**Customer:** Incident reviews. Every time we have a postmortem, I lose a
day writing up what happened, what we changed, who was affected. The format
keeps changing. Last quarter we had three different templates. The leads
want consistency, the engineers want the form to be shorter. Nobody's
happy. I'd love a way to just... talk through what happened and have the
writeup assemble itself.

**Interviewer:** If you could change one thing about Monday mornings, what
would it be?

**Customer:** Just give me a queue, sorted by what's been waiting longest,
with enough context that I can decide whether to review it or hand it off
to someone better suited. That's it.
