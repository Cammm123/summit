# What you need, and free alternatives

Checked November 2026. Claude's plans and features change often, so confirm on
[claude.com/pricing](https://claude.com/pricing) and in the
[Claude Code docs](https://code.claude.com/docs/en/desktop-scheduled-tasks) before you
pay for anything.

## Disclaimer: the full version of Summit needs a paid Claude plan

Summit uses three Claude features together. All three need a paid plan:

1. **Claude Code in the desktop app.** Setup and the daily morning run happen in
   Claude Code. Anthropic's pricing page lists Claude Code on **Pro** ($20 a month, or
   $17 a month billed yearly) and **Max** (from $100 a month), and **not on Free**.
   Team and Enterprise seats can include it, depending on the seat type and on your
   admin.
2. **Local scheduled tasks.** The morning run is a scheduled task in the desktop app
   (version 1.1.5368 or later). It runs only while the app is open and your computer is
   awake. If the computer sleeps through the run time, the app does one catch-up run
   when it wakes. Turning on **Keep computer awake** in the app's settings helps.
   Scheduled tasks are marked as a research preview.
3. **Artifacts that save data and ask Claude.** The mountain page keeps your levels
   and answers in the artifact's own storage and grades answers by asking Claude.
   Artifacts can be made on the Free plan, but saved artifact data isn't available there
   (reported as a paid-plan feature). Grading on the page counts against **your own**
   usage.

Summit itself is free and open source (MIT). You pay only for your Claude plan.
Anthropic doesn't list an individual student discount on its pricing page; some
schools have an institution-wide Claude for Education plan, so ask your school.

**What happens if something is missing**

| You have | What Summit does |
|---|---|
| All three | The full mountain page with instant grading, plus the morning check. |
| Claude Code and scheduled tasks, but artifacts can't save data | Each morning the quiz is posted in a Claude Code chat; you answer there and Claude grades it. No mountain page. |
| Claude Code but no scheduled tasks | Say "today's Summit level" whenever you want to study; same quiz, no automatic morning run. |
| Free plan | Use **Summit Lite** or one of the free tools below. |

This repo isn't affiliated with Anthropic.

## Free alternatives

| Option | Cost | What it does well | Missing compared with Summit |
|---|---|---|---|
| **Summit Lite** (this repo, [`lite/daily-prompt.md`](../lite/daily-prompt.md)) | Free with Claude Free, ChatGPT or Gemini | The same daily quiz rules and diagnostic grading, as one prompt you paste into any chatbot with your schedule and notes. | No mountain, no automatic morning run, and you keep your own weak-spot list. |
| **[NotebookLM](https://notebooklm.google.com)** (Google) | Free, with daily limits | Upload your slides and notes; it makes flashcards and practice quizzes only from your sources. | No exam-date plan or spaced repetition across days; reported free limit of about 10 quiz/flashcard sets a day. |
| **ChatGPT "Study and learn" mode** | Free tier | Step-by-step tutoring that asks questions instead of giving answers. | No schedule, no saved weak spots between chats unless you paste them back. |
| **[Anki](https://apps.ankiweb.net)** | Free on Mac, Windows, Linux, Android and the web (the iPhone app is paid) | Best-in-class spaced repetition for facts and definitions. | You write the cards; no grading of explanations. |
| **[RemNote](https://www.remnote.com)** | Free tier | Notes that turn into flashcards with spaced repetition. | AI features are limited on the free tier. |
| **[Quizlet](https://quizlet.com)** | Free tier | Flashcards and quick practice tests; many shared sets. | AI features and some test modes are limited on the free tier. |

Free-tier limits change often; check each tool's own pages.

## Sources

- [Claude pricing](https://claude.com/pricing): plans, prices and which include Claude Code.
- [Schedule recurring tasks in Claude Code Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks): app version, run conditions, missed runs.
- [Automate work with scheduled tasks (cloud)](https://code.claude.com/docs/en/routines): plans that have scheduled tasks.
- Artifact storage on paid plans (third-party write-ups): [Caipi](https://caipi.ai/blog/can-claude-artifacts-save-data), [Charming](https://usecharming.com/do-claude-artifacts-save-data).
- NotebookLM quizzes and limits (third-party): [BibiGPT](https://bibigpt.co/en/features/notebooklm-flashcards-quizzes-explained).
- ChatGPT Study Mode (third-party): [Reskilll](https://blogs.reskilll.com/best-free-ai-study-tools-students-2026/).
