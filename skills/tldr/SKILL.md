---
name: tldr
description: >
  Direct, high-signal, zero-fluff technical explanations. Explains code, architecture,
  functions, or technical concepts concisely using the BLUF (Bottom Line Up Front) model,
  structured bullet points, and exact code links without conversational filler or bloated preambles.
  Use when user asks for brief explanations ("jelasin singkat", "to the point", "tldr",
  "nggak perlu bertele-tele", "no verbose", "summary", "explain briefly"), or invokes /tldr.
license: MIT
metadata:
  author: WahyuS002
  version: 1.0.0
  category: productivity
  tags: [explanation, conciseness, developer-tools, communication]
---

# TLDR (To The Point & Zero-Fluff)

Delivers crystal-clear, high-density technical explanations stripped of all pleasantries, preambles, and conversational filler. Maximizes signal-to-noise ratio.

## Quick start

```text
/tldr                              # Explain current context or recent changes to the point
/tldr <file_path>                  # Explain the purpose and flow of a specific file
/tldr <symbol_or_function>         # Explain a specific function, class, or method
/tldr <technical_concept>          # Explain a concept/protocol (e.g. /tldr sqlite wal, /tldr cgnat)
```

---

## Instructions

### Step 1: Ingest & Target Resolution
1. Identify the target concept, file, or symbol.
2. If given a file path or symbol, read the relevant lines using code reading tools.
3. If given a broad concept, identify its single most critical mechanism before writing.

### Step 2: Formulate BLUF (Bottom Line Up Front)
1. Write **1–2 sentences** stating strictly what the entity does and its primary utility.
2. Avoid generic intros (e.g., do NOT start with "Sure, here is...", "This function is designed to...").

### Step 3: Extract Core Mechanics (3–5 Bullets)
1. List 3 to 5 chronological or structural steps explaining how it works under the hood.
2. Bold the primary action keyword at the beginning of each bullet.
3. Highlight critical branch conditions, fallbacks, or state changes.

### Step 4: Precision Code Referencing & Fluff Removal
1. Attach exact file links with line ranges (e.g., `[main.go#L20-L40](file:///path/to/main.go#L20-L40)`).
2. Scan output and remove all conversational fillers, pleasantries, and sign-offs.

---

## The 3-Layer Response Framework

Every explanation generated must adhere to this structure:

1. **BLUF (Bottom Line Up Front)**: Exactly 1–2 sentences defining the core purpose.
2. **Core Mechanics**: 3–5 bullet points detailing the step-by-step mechanism.
3. **Precision References / Edge Cases**: Clickable file & symbol links, plus any crucial fallback behavior.

---

## Anti-Patterns (Strictly Prohibited)

- ❌ **Conversational fluff:** "Tentu!", "Dengan senang hati!", "Pertanyaan yang sangat bagus!", "Berikut adalah penjelasannya...".
- ❌ **Closing filler:** "Semoga penjelasan ini membantu!", "Kabar saya jika ada pertanyaan lain!".
- ❌ **Code dump:** Pasting large blocks of unmodified code that the user already has open or can view via link.
- ❌ **Narrative drift:** Tangents into historical context or lore unless explicitly requested.
- ❌ **Over-explaining basics:** Explaining basic language syntax when explaining architecture or high-level methods.

---

## Examples

### Example 1: Explaining a function
**User says:** "bisa jelasin apa itu persist() di monitoring/main.go? singkat aja, ga usah bertele-tele"

**Actions:**
1. Inspect `monitoring/main.go` around `func (c *collector) persist(...)`.
2. Extract core purpose: saving metrics batch to SQLite.
3. Identify key steps: cleanup expired -> batch insert -> auto prune fallback.

**Result:**
> Method [`persist()`](file:///path/to/main.go#L211-L250) di [main.go](file:///path/to/main.go) berfungsi untuk **menyimpan data metrik kontainer ke database SQLite secara berkala dalam satu transaksi**.
> 
> **Alur kerja:**
> 1. **Pembersihan data kadaluarsa:** Memanggil [`deleteExpired()`](file:///path/to/main.go#L252-L255) untuk menghapus data yang melewati batas retensi.
> 2. **Simpan batch metrik:** Menulis seluruh `samples` ke tabel `deployment_metrics` (`INSERT OR REPLACE`).
> 3. **Penanganan kapasitas penuh:** Jika penulisan gagal karena `"full"`, memanggil [`pruneOldest()`](file:///path/to/main.go#L257-L269) untuk memangkas 10% data terlama lalu mencoba simpan kembali.

---

### Example 2: Explaining a concept
**User says:** "apa itu SQLite WAL?"

**Result:**
> **SQLite WAL (Write-Ahead Logging)** adalah mode penjurnalan di mana **perubahan data ditulis ke file `.wal` terpisah sebelum digabungkan ke database utama**, memungkinkan pembacaan dan penulisan berjalan bersamaan (*concurrent read-write*).
> 
> **Poin kunci:**
> - **Concurrent Reads:** Reader tidak memblokir writer, dan writer tidak memblokir reader.
> - **Checkpointing:** Data di file WAL secara periodik disinkronkan (*flushed*) kembali ke file `.db` utama.
> - **Performance:** Menghilangkan overhead locking penuh pada file database saat transaksi tulis berlangsung.

---

## Troubleshooting

### Target is too broad or ambiguous
- **Cause:** User asked "/tldr this project" or a very broad query without specifics.
- **Solution:** Provide a 2-sentence architecture BLUF + 4 main component bullets, then provide short slash command suggestions to inspect specific submodules.

### Code file not found
- **Cause:** Typo in file path or symbol name.
- **Solution:** State in 1 sentence that the file/symbol was not found, list up to 3 closest matches, and ask for target clarification without conversational filler.

---

## Rules

1. **Maximum Density:** Every word must convey functional meaning. Remove any sentence that does not directly aid understanding.
2. **Grounding & Links:** Always use markdown links pointing directly to the relevant file and line range (`[file.go#L1-L20](file:///path/to/file.go#L1-L20)`).
3. **Respect Language of Prompt:** If the user asks in Indonesian, answer in concise Indonesian. If English, answer in concise English.
4. **No Premature Follow-ups:** Do not ask unnecessary open-ended closing questions unless clarification is strictly required to proceed.
