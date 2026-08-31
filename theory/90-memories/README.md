# Memories

**This folder is where anything worth remembering between sessions is written.**
Not a private directory outside the repository — here, in git, where the user
can read it, review it, correct it, and where it travels with the project to
every machine and every future session.

## The format

One fact per file. Filename is the slug: `kebab-case-name.md`.

```markdown
---
name: <kebab-case-slug, same as the filename>
description: <one line — what this is, so its relevance is obvious at a glance>
type: project | decision | pitfall | preference | reference
date: YYYY-MM-DD
---

The fact itself, stated in present tense, as something that is true now.

**Why:** the reasoning, or what went wrong that made this worth recording.
**How to apply:** what a future session should actually do about it.

Related: [[other-memory-slug]]
```

`type` values:

| Type | For |
|---|---|
| `project` | Ongoing work, goals, constraints not derivable from the code |
| `decision` | A choice that was made and the reasoning behind it, so it is not silently reversed |
| `pitfall` | Something that went wrong and how to avoid repeating it |
| `preference` | How the user wants things done, and why |
| `reference` | Pointers to external resources, formats, specs |

## Rules

1. **One fact per file.** If a file is about two things, split it.
2. **Check for an existing file first.** Update it rather than creating a
   near-duplicate.
3. **Delete memories that turn out to be wrong.** A stale memory is worse than
   no memory.
4. **Do not record what the repository already records.** Code structure, past
   fixes, commit history and anything in `CLAUDE.md`/`AGENTS.md` are already
   written down. Record what is *not* derivable from them.
5. **Absolute dates only.** "Last Tuesday" is meaningless six months later.
6. **Present tense.** State the invariant, not the story of how it was learned —
   the reasoning belongs in **Why**, and the history belongs in the commit
   message.
7. **Add the `@` import** for every new memory file to the list at the bottom of
   `AGENTS.md`, in the same commit — otherwise it is not loaded and it does not
   exist as far as the next session is concerned.
8. **No secrets.** No credentials, tokens, keys or private paths.

## Why this folder sorts last

It is `90-` so it comes after every theory section. The theory library
(`00-` to `40-`) is general public knowledge that would be true in any project;
this folder is the opposite — everything specific to *this* project and *this*
user that has been learned along the way.
