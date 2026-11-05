---
name: summit-setup
description: First-time setup of Summit for one course. Checks the student's Claude setup, interviews them about the course, creates my-course/, publishes their own mountain page, creates the daily scheduled task, and makes the first level. Use when someone says "set up Summit", "start Summit", or opens this repo with no my-course/course.md.
---

# Set up Summit

Goal: by the end the student has their course files in `my-course/`, their own private
Summit page, a daily morning task, and a first level they can open right away. Work
through the steps in order and keep them informed with one short line per step.
Be friendly and brief; they're a student, maybe not technical.

If `my-course/course.md` already exists, ask whether to **update** it (change dates,
add an exam, move the run time) or **start over** for a new course (move the old
folder to `my-course-old-<date>/` first). Summit runs one course per folder; for a
second course, clone the repo again into another folder.

## 1. Check requirements

Find out what this setup can do, and tell the student plainly. Don't guess: look.

| Check | How | If missing |
|---|---|---|
| Running in Claude Code | You can run shell commands and edit files here. | Point them to `lite/daily-prompt.md` (Summit Lite) and `docs/requirements.md`, then stop. |
| Scheduled tasks | A `create_scheduled_task` tool exists (ToolSearch `scheduled task`). | Delivery `manual`: they say "today's Summit level" each day. |
| Artifacts with saved data | A tool that publishes artifacts **and** a tool that writes artifact data (ToolSearch `publish artifact`, `db_write`, `ArtifactData`). The claude-artifacts MCP has `publish_files`, `declare_capabilities`, `db_write`; the built-in `Artifact` tool publishes with `capabilities` and `ArtifactData` writes data. | Delivery `chat`: the morning run posts the quiz in chat. |
| Tools to read materials | `pdftotext -v` (poppler). | Suggest installing poppler (`brew install poppler` on Mac); the Read tool can still read PDFs page by page. |

If artifacts look available, the real test is step 5: if publishing or declaring
`db` is refused (for example on a plan without saved artifact data), switch to delivery
`chat` and say so. Summarize in one line, e.g. "Everything's here: you'll get the full
mountain page with a 7 AM daily level."

## 2. Interview

Use the AskUserQuestion tool for choices if you have it; ask the open questions in
chat. Ask in a few small rounds, not one wall of questions. Accept pasted syllabi,
schedule screenshots or files: read them and fill in what you can, then confirm.

1. **Course:** name (and number), subject, and the student's first name (optional; it
   personalizes the feedback).
2. **How it's tested:** what exam questions look like (definitions and recall, mechanisms
   and processes, calculations, proofs, applying ideas to new scenarios, essays, coding,
   diagrams). From this, propose `question_styles` (3–5 types) and `gap_terms` (how to
   name mistakes in this subject), and confirm them.
3. **Assessments:** every quiz, exam and final still ahead, with dates and what each
   covers (lecture numbers or topics). A final with no date yet is fine ("TBD").
4. **Lectures:** the lecture list with dates, if they have it (past and upcoming).
5. **Materials:** ask them to put slides or notes in `my-course/materials/` (PDF is
   best; subfolders per unit are fine). Create the folder first and tell them its full
   path. Continue while they do it.
6. **Study time and run time:** minutes per day (default 30) and when the daily level
   should be ready (default 7:00 AM, local time). Mention that the computer must be
   awake then, or the run catches up when it wakes.
7. **Feedback style:** tutor (explains the gap and the idea, offers more; the default)
   or full worked answers right away. And plain-words-first explanations, yes or no.
8. **Breaks:** any holidays or weeks off ahead.

## 3. Create my-course/

- Copy `templates/` into `my-course/` (keep the `notes/` folder) and create
  `my-course/materials/` and `my-course/levels/`.
- Fill in `course.md` from the interview (`setup_date` = today, `delivery` from step 1),
  `schedule.md` (assessments, lectures, breaks), and `deadlines.md` (every assessment
  under Upcoming).
- Confirm `my-course/` is ignored: `git check-ignore -q my-course && echo ignored`.

## 4. Map the materials

For each file in `my-course/materials/`, add a row to `notes/slide-map.md`: topics by
slide or page number and where any practice questions are (topics and page numbers
only, never slide text). Match files to lectures in `schedule.md` (fill the `File`
column). If nothing is there yet, say the first level will use what they've told you
and the next ones will use the slides once they're added.

## 5. Publish their page (delivery `page`)

1. Publish `app/index.html` as a **new private** artifact on their account, title
   `<Course> Summit` (e.g. "Biology Summit"), icon `mountain`:
   - claude-artifacts MCP: `publish_files` with `files: [{as: "index.html", path: "<absolute path to app/index.html>"}]`, `title`, `icon`;
   - built-in Artifact tool: publish `app/index.html` with that title.
2. Declare its capabilities:
   `{"db": {"rules": [{"path": "", "read": "view", "write": "owner"}]}, "sample": {}, "user": {}}`
   (claude-artifacts: `declare_capabilities` with the version from the publish result;
   built-in: pass `capabilities` on the publish).
3. Write `meta/path`: `title` (same as the page title), `course`, `student`,
   `tutorStyle`, `gapTerms`, and `nodes`: one per day from today to the next exam
   (`kind: "day"`; quiz days `kind: "camp"` with `sub` = the quiz name; the exam
   `kind: "peak"` with `sub`). If the next exam is more than 40 days away, end the
   mountain at the last quiz before day 40 and make that the peak.
4. Save `page_url` and `page_slug` in `course.md`.

If any of these is refused, set `delivery: chat` in `course.md`, tell the student in one
line why, and continue.

## 6. Create the daily task

With `create_scheduled_task`:
- `taskId`: `summit-<short-course-slug>` (e.g. `summit-bio-121`); `title`:
  "Summit: <course>"; `cronExpression` from the run time (07:00 → `0 7 * * *`);
  `description`: "Daily Summit level for <course>".
- `prompt` (fill in the absolute path of this repo folder):
  ```
  Work in the folder <ABSOLUTE PATH TO THIS REPO>. Read its CLAUDE.md, then follow
  .claude/skills/summit-daily/SKILL.md exactly for today's Summit level. The student
  isn't watching live: don't ask questions; make reasonable choices and note them.
  ```
Then tell the student: open the task in the desktop app's **Scheduled** page and click
**Run now** once tomorrow morning (or now), and choose "always allow" on the permission
prompts, so later runs don't stall waiting for approval. Delivery `manual`: skip the
task and tell them to say "today's Summit level" each day.

## 7. First level

Run the `summit-daily` skill now for today (steps 2–4; nothing to sync yet). Then show
the student:
- the page link and one line on what to do ("Click the bouncing level, read the
  primer, answer one question at a time");
- that the first time they submit, the page asks permission to use Claude for grading,
  and grading uses their own Claude usage;
- what happens each morning, and that they can change anything by editing
  `my-course/course.md` or telling Claude ("move my exam to Friday").

## Notes

- Never publish the page publicly or share it; it's private to the student.
- Never commit `my-course/`.
- If they give a date without a year, assume the current school year.
