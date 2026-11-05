# How Summit works

## The pieces

1. **The page** (`app/index.html`) is published once, by setup, as a private artifact on
   the student's claude.ai account. It declares three runtime capabilities:
   - `db`: the artifact's own document database (levels, answers, checkpoints);
   - `sample`: lets the page ask Claude to grade an answer, answer a follow-up, or write
     the end-of-level checkpoint;
   - `user`: who is viewing (used only to check write access).
   Database rule: everyone who can open the page can read; only the owner writes
   (`{"path": "", "read": "view", "write": "owner"}`). Only the student opens it.
2. **The morning task** is a local scheduled task in the Claude desktop app. Its prompt
   is one line: run the `summit-daily` skill in this folder. So a `git pull` of this
   repo improves the routine without touching the task.
3. **The course files** in `my-course/` hold the schedule, the materials and Claude's
   notes about the student. They never leave the student's computer except as the
   levels Claude writes to their own page.

## Database layout

| Document | Written by | Fields |
|---|---|---|
| `meta/path` | Claude | `title` (page heading), `course`, `student` (first name, optional), `tutorStyle`, `gapTerms`, `nodes: [{date: "YYYY-MM-DD", kind: "day" \| "camp" \| "peak", sub?: "Quiz 3"}]` |
| `levels/YYYY-MM-DD` | Claude | `date`, `target` ("Quiz 3"), `daysLeft`, `why`, `primer?: [{h, body}]`, `questions: [{id: "q1", tag?, text, key: {mechanism, mustHave[], traps[], slides}}]` |
| `answers/YYYY-MM-DD_qN` | page, then Claude | `date`, `qid`, `tag`, `answer`, `verdict` (`right` \| `partial` \| `wrong` \| `skipped` \| `pending`), `gotRight`, `gap`, `mechanism`, `slides`, `gradedBy` (`page` \| `key` \| `claude`), `followups?: [{q, a}]` |
| `checkpoints/YYYY-MM-DD` | page or Claude | `date`, `text`, `gradedBy` |

`key.mechanism` is the full correct answer with its explanation (the field name stays
from the first, biology version; it's used for any subject). All text is plain text.

## A level, step by step

1. The page lists `meta/path` nodes along the ridge. A node with a `levels/` document is
   open; with every question answered it's done; without a document it's locked.
2. The student opens a level: the primer (if any), then one question at a time. Drafts
   are kept in the browser while typing.
3. **Submit** saves the answer as `pending`, asks Claude (through `sample`) to grade it
   against the key, and saves the verdict, gap and explanation. **Skip** saves
   `skipped` and shows the key's explanation.
4. Under each graded answer the student can ask follow-ups; they're saved on the answer.
5. After the last question the page writes a 1–2 line checkpoint.

## The morning check

Every morning `summit-daily`:
1. re-grades each answer not yet `gradedBy: "claude"`, against the key **and the slides**,
   overwrites anything the page got wrong, and fixes misleading follow-up replies;
2. updates `my-course/notes/` (weak spots, quiz log, lectures reviewed);
3. picks today's questions by phase (normal day, new material, day before a quiz, quiz
   day, exam build-up, breaks, final) and writes `levels/<today>`;
4. keeps the mountain going: after an exam passes, `meta/path` starts a new mountain
   up to the next exam.

## Why grading can be off, and how it's caught

The page's grader never sees the slides, only the key. A thin key means loose grading.
That's why the daily skill spends most of its care on keys (`mustHave`, `traps`) and
why the morning check re-grades with the slides open. Answers it changed show
"Checked by Claude".
