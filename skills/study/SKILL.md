---
name: study
description: >
  Interactive active-recall learning and note distillation session. The agent explains complex
  technical concepts with official documentation/RFC references and optional CLI experiments,
  drills the user with adaptive active-recall questions (scaled to topic complexity, max 5),
  rewords the user's responses into structured Markdown cheat sheets, and commits them to
  ~/Documents/notes/<category>/.
---

# Study

Active-recall learning session that turns technical concepts, codebase patterns, and official RFCs into deeply understood personal knowledge base notes.

## Quick start

```text
/study                         # Ask what concept or file to study
/study <topic>                 # Study a specific concept (e.g. /study cgnat, /study docker-socket)
/study <file_path>             # Study logic/patterns from a specific codebase file
```

## Setup & Prerequisites (Dynamic & Configurable)

1. **Detect / Ask Notes Target Directory:**
   - Do not hardcode a single path. Check for common notes locations:
     - `~/Documents/notes`
     - `./docs/` or `./notes/` within the current workspace
   - If ambiguous or on first run without an obvious notes folder, ask the user:
     > *"Where would you like to save your study notes? (e.g. `~/Documents/notes`, `./docs/notes`, or custom path)"*
   - Remember the selected path for the remainder of the session.

2. **Category Routing:**
   - Organize notes into logical subdirectories under the target notes path (e.g., `<target_notes_dir>/<category>/<NN-slug>.md`).
   - Automatically create missing category directories as needed.

3. **Safe Git Persistence (Conditional):**
   - Check if the chosen notes directory is inside a Git repository (`git rev-parse --is-inside-work-tree`).
   - **If Git is initialized:** Automatically stage and commit the note (`git add` + `git commit`).
   - **If Git is not initialized:** Save the Markdown note file safely without attempting Git commands.

---

## Workflow

### Step 1 — Identification & Grounding (Theory & Experiments)

1. **Understand the Target Topic:**
   - If a file/code snippet is passed, read it with `view_file` or code search tools.
   - If a general technical topic is passed, search official documentation or IETF RFCs with `search_web`.
2. **Explain with Clarity & Precision:**
   - Break down the theory using simple analogies, ASCII diagrams, comparison tables, and code snippets.
   - **Grounding Rule:** Always ground claims in official documentation (e.g., IETF RFCs, Docker Specs, Go Standard Library docs).
3. **Optional Hands-on CLI Experiment:**
   - If the concept involves CLI commands, networking interfaces, or system tools, provide step-by-step commands for the user to try in their terminal.

---

### Step 2 — Active Recall Question Drill & Interactive Evaluation

1. **Adaptive Question Generation:**
   - Generate focused active-recall questions (jumlah adaptif disesuaikan dengan kompleksitas topik: 2–3 soal untuk konsep spesifik/sederhana, hingga maksimal 5 soal untuk topik luas/arsitektur) covering core principles, syntax, security implications, edge cases, and practical code implementations.
   - Jangan memaksakan 5 soal jika topik sudah tuntas dalam 2–3 soal.

2. **Evaluate & Give Precise Feedback on Each Answer:**
   - **Jika Benar:** Konfirmasi dan beri penguatan singkat atas poin-poin kuncinya.
   - **Jika Setengah Benar / Kurang Lengkap:** Tunjukkan dengan jelas bagian mana yang sudah tepat, lalu beri klarifikasi/elaborasi pada bagian yang masih rancu agar pemahaman user utuh.
   - **Jika Salah / Terjadi Miskonsepsi:**
     - **JANGAN langsung membuat notes!**
     - Berikan penjelasan yang membimbing (*guided explanation*) dan arahkan ke pemahaman yang benar.
     - **Wajib minta user untuk menjawab ulang (*re-attempt*)** pertanyaan yang salah tersebut sebelum melangkah ke proses pembuatan catatan.

3. **Deep-Dive Pause:**
   - Jika user bertanya atau kesulitan di tengah drill, jeda sesi tanya jawab, jelaskan konsepnya (atau berikan eksperimen mini), lalu lanjutkan saat user siap.

---

### Step 3 — Note Distillation & Structuring

1. Take the user's validated answers and reword them into a professional, highly structured Markdown cheat sheet.
2. Include the following sections in the note:
   - `# Cheat Sheet: <Topic Title>`
   - `## 1. <Core Definition & Background>`
   - `## 2. <Architecture / Syntax / Comparison Table>`
   - `## 3. <Practical Code / Command Usage>`
   - `## 4. <Security & Edge Cases>`
   - `## Referensi Terkait` (Verified links + relative links to existing notes).
3. **Formatting Quality Rule:**
   - Keep lines clean and readable.
   - Use standard code blocks (`text`, `go`, `bash`) for math or code equations instead of nested math markers inside bold text.

---

### Step 4 — File Writing & Git Auto-Commit

1. Determine the sequential prefix number based on existing files in `<target_notes_dir>/<category>/` (e.g., `01-`, `02-`, `03-`, `04-`).
2. Save the note to `<target_notes_dir>/<category>/<NN-slug>.md`.
3. If `<target_notes_dir>` is a Git repository, execute Git commands:
   ```bash
   git add <category>/<NN-slug>.md
   git commit -m "docs: add <NN-slug>.md note"
   ```
4. Present a summary of the created note path and git status to the user.

---

## Rules

- **Strict Drill Completion & No Premature Notes:** Jangan pernah menulis note sebelum seluruh pertanyaan drill dijawab dengan benar oleh user. Jika ada jawaban salah, berikan arahan dan minta user menjawab kembali.
- **Explicit Feedback on Partial Answers:** Berikan klarifikasi eksplisit pada jawaban yang setengah benar agar user mengetahui dengan jelas letak benar/salahnya.
- **Adaptive Questions (Max 5):** Sesuaikan jumlah pertanyaan dengan kompleksitas materi (2–3 untuk konsep terfokus, maksimal 5 untuk topik luas).
- **Configurable Destination:** Always check or ask for the user's preferred notes directory (`<target_notes_dir>`). Do not force a single hardcoded path.
- **Reference Grounding:** Always verify external facts (RFC numbers, CLI syntax, standard library behaviors) before asserting them.
- **No Silo Notes:** Always include a `Referensi Terkait` section with relative Markdown links to related notes in `<target_notes_dir>`.
- **Safe Persistence:** Stage and commit notes only if the target notes folder is a Git repository; otherwise, save the file cleanly.
