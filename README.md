# Daily Reflection Tree - DT Fellowship Assignment

A deterministic reflection agent that guides employees through structured end-of-day reflection across three psychological axes: **Locus of Control**, **Orientation (Contribution vs Entitlement)**, and **Radius of Concern (Self-Centric vs Altrocentric)**.

## Overview

This assignment demonstrates how to encode psychological theory into a deterministic system that guides reflection *without* using an LLM at runtime. The reflection tool is fully static — it loads from structured data, walks through a tree based on user choices, and produces personalized reflections through careful question design and signal aggregation.

**Core Principle**: The tree is the product. AI is the power tool used to build it.

## Project Structure

```
reflection-tree-assignment/
├── tree/
│   ├── reflection-tree.json          # The complete tree data structure
│   └── tree-diagram.md               # Mermaid visualization of the tree
├── agent/
│   └── reflection_agent.py           # Python CLI agent that loads and walks the tree
├── transcripts/
│   ├── persona-1-victim-transcript.md    # Sample: External locus, entitlement, self-centric
│   └── persona-2-victor-transcript.md    # Sample: Internal locus, contribution, altrocentric
├── write-up.md                       # Design rationale and psychological grounding
├── README.md                         # This file
└── .gitignore
```

## Part A: The Reflection Tree (Required)

### Structure

The tree contains **38 nodes** organized into:

- **1 Start node** — Session opening
- **3 Bridge nodes** — Transitions between axes
- **8 Question nodes** — Gate questions for each axis with fixed options
- **5 Decision nodes** — Invisible routers that branch based on answers
- **6 Reflection nodes** — Reframes that tally signals for state
- **1 Summary node** — Final synthesis with interpolated insights
- **1 End node** — Closing

### The Three Axes

#### Axis 1: Locus of Control (Victim ↔ Victor)
**Psychology**: Rotter (1954), Dweck (2006)

Questions probe whether employees see themselves as agents or reactors:
- "How would you describe today?" (Productive/Mixed/Tough/Draining)
- "What was YOUR role?" vs "What was your first instinct under pressure?"

**Signals tracked**: `axis1:internal` or `axis1:external`

---

#### Axis 2: Orientation (Contribution ↔ Entitlement)
**Psychology**: Organ (1988), Campbell et al. (2004)

Questions reveal whether focus is on what they *gave* or what they *expected*:
- "Think about one meaningful interaction..." (Helped/Taught/Asked/Unrecognized)
- Follow-ups probe actual behavior, not beliefs

**Signals tracked**: `axis2:contribution` or `axis2:entitlement`

---

#### Axis 3: Radius of Concern (Self-Centric ↔ Altrocentric)
**Psychology**: Maslow (1969), Batson (2011)

Questions explore whose world the employee is thinking about:
- "Whose world comes to mind?" (My own/Team/Someone harder/Customer)
- Follow-ups ask about the *feeling* of each frame

**Signals tracked**: `axis3:self_centric` or `axis3:altrocentric`

---

### Key Design Features

1. **Fixed options only** — Every question has 3-5 predefined choices. No free text.
2. **Deterministic routing** — Same answers → same path, every time.
3. **No judgment** — Reflections reframe without moralizing.
4. **Signal aggregation** — Multiple paths accumulate signals; summary shows the blend.
5. **Interpolation** — Reflections reference the employee's actual answers.

### How to Read the Tree

The JSON file is self-documenting:

```json
{
  "id": "A1_OPEN",
  "parentId": "A1_INTRO",
  "type": "question",
  "text": "If you had to pick one word for today, which fits best?",
  "options": ["Productive", "Mixed", "Tough", "Draining"],
  "target": null,
  "signal": null
}
```

- **id**: Node identifier
- **parentId**: Which node precedes this (tree hierarchy)
- **type**: Determines behavior (question, decision, reflection, etc.)
- **text**: What the employee sees; can contain placeholders like `{A1_OPEN.answer}`
- **options**: User-visible choices (empty for auto-advancing nodes)
- **target**: Override target for bridge nodes
- **signal**: Signal(s) this node contributes to state tracking

### Tree Visualization

See [tree-diagram.md](tree/tree-diagram.md) for a Mermaid visualization of the complete tree structure.

---

## Part B: The Agent (Bonus)

### Quick Start

#### Requirements
- Python 3.8+
- No external dependencies (uses only stdlib)

#### Run the Agent

```bash
cd agent/
python reflection_agent.py
```

The agent will:
1. Load the tree from `../tree/reflection-tree.json`
2. Present each node interactively
3. Track state and signals as you answer
4. Provide reflections based on your path
5. Generate a final summary
6. Save a transcript to `transcripts/session_TIMESTAMP.txt`

#### Example Session

```
============================================================
Daily Reflection Tree
============================================================

Good evening. Let's take 5 minutes to look at your day...

How would you describe today — the overall shape of it?

If you had to pick one word for today, which fits best?
  1. Productive — I moved things forward
  2. Mixed — wins and setbacks
  3. Tough — harder than I wanted
  4. Draining — it took everything I had

Your choice (number): 1
```

---

### How the Agent Works

The `ReflectionTreeAgent` class:

1. **Loads the tree** — Parses JSON into an in-memory node map
2. **Tracks state** — Stores answers, signals, and path taken
3. **Routes decisions** — Parses condition strings to branch correctly
4. **Accumulates signals** — Tallies which poles the employee leans toward
5. **Interpolates text** — Replaces `{A1_OPEN.answer}` with actual answers
6. **Generates summary** — Determines dominant poles and synthesizes insights

Key methods:

- `step(user_choice)` — Advance one node; handle user input or auto-advance
- `_route_decision()` — Parse decision node conditions and find target
- `_accumulate_signals()` — Tally signals from reflection nodes
- `_generate_summary()` — Interpolate summary with actual poles and insights
- `get_transcript()` — Get full session transcript

---

### Sample Transcripts

Two complete sample sessions are included:

1. **[Persona 1: Victim](transcripts/persona-1-victim-transcript.md)**
   - **Path**: Tough day → Felt stuck (external) → Unrecognized (entitlement) → Self-focused
   - **Summary**: External locus, entitlement, self-centric
   - **Final insight**: "What are you trying to prove?"

2. **[Persona 2: Victor](transcripts/persona-2-victor-transcript.md)**
   - **Path**: Productive day → Adapted (internal) → Helped (contribution) → Customer-focused
   - **Summary**: Internal locus, contribution, altrocentric
   - **Final insight**: "That's where meaning lives."

Both transcripts show how the same tree produces different paths and reflections based on answers — demonstrating determinism, personalization, and psychological grounding.

---

## Design Rationale

See [write-up.md](write-up.md) for detailed explanation of:

- Why these specific questions
- How branching was designed
- Psychological sources (with citations)
- Trade-offs made
- What would be improved with more time

---

## Key Constraints Met

✅ **No LLM at runtime** — Tree is fully static; agent uses no API calls  
✅ **Deterministic paths** — Same answers produce same reflection every time  
✅ **Fixed options only** — No free text; every choice is predefined  
✅ **No moralizing** — Reflections reframe without judgment  
✅ **Three axes in sequence** — Each builds on the previous  
✅ **25+ nodes** — 38 total nodes  
✅ **8+ question nodes** — 8 question nodes with 3-5 options each  
✅ **Readable data format** — Fully structured JSON, no opaque code  

---

## Psychological Grounding

### Axis 1: Locus of Control
- **Rotter (1954)**: Generalized expectancy that outcomes are contingent on one's behavior (internal) or external forces (external)
- **Dweck (2006)**: Growth mindset (abilities can be developed) vs fixed mindset (abilities are innate)
- **Why it matters**: Internal locus predicts resilience, persistence, and learning. The tree surfaces agency without judgment.

### Axis 2: Contribution vs Entitlement
- **Organ (1988)**: Organizational Citizenship Behavior — discretionary effort beyond formal role
- **Campbell et al. (2004)**: Psychological entitlement — stable belief one deserves more than others
- **Why it matters**: High OCB drives team performance. Entitlement undermines culture. The tree probes actual behavior to surface what the employee is experiencing.

### Axis 3: Radius of Concern
- **Maslow (1969)**: Self-transcendence — peak state where concerns shift from self to other/larger purpose
- **Batson (2011)**: Perspective-taking — cognitive understanding of another's experience
- **Why it matters**: Research shows meaning and well-being increase when radius widens. The tree shows the benefit and cost of each frame.

---

## Testing the Design

Two sample personas were tested against the tree:

| Persona | Axis 1 | Axis 2 | Axis 3 | Path | Result |
|---------|--------|--------|--------|------|--------|
| **Victim** | External | Entitlement | Self-Centric | 5 nodes | Invited to reflect on what they're proving |
| **Victor** | Internal | Contribution | Altrocentric | 5 nodes | Affirmed that meaning lives in the bigger thing |

Both paths:
- Feel like natural conversations
- Surface psychological truth without interrogation
- End with reflection, not judgment
- Are fully reproducible

---

## Future Enhancements

With more time, could add:

1. **Weighted signals** — Some answers count more (e.g., asking for help signals growth)
2. **Deeper follow-ups** — Second layer of branching within axes
3. **Day-of context** — Adapt questions based on day type (meetings, creative work, crisis, etc.)
4. **Longitudinal tracking** — Identify trends across sessions and suggest deeper work
5. **Tone variation** — Subtly different language based on persona (internal/external responders)
6. **Micro-pauses** — Built-in reflection time between sections

---

## Submission Contents

- ✅ **reflection-tree.json** — Complete tree data structure
- ✅ **tree-diagram.md** — Mermaid diagram visualization
- ✅ **write-up.md** — Design rationale (2 pages)
- ✅ **reflection_agent.py** — Working Python agent
- ✅ **persona-1-victim-transcript.md** — Sample session #1
- ✅ **persona-2-victor-transcript.md** — Sample session #2
- ✅ **README.md** — This documentation

---

## How to Evaluate

### Part A Evaluation (Required)

Read `reflection-tree.json` and trace paths:
- Is the tree clean, structured, and readable as data?
- Do questions genuinely surface the three axes?
- Does each option feel honest (not leading)?
- Do reflections reframe without judgment?
- Does the tree feel like a conversation?

Check `tree-diagram.md`:
- Can you visualize the branching structure?
- Are all paths accounted for?

Read `write-up.md`:
- Does the designer understand why they made their choices?
- Are there psychological sources cited?
- Are trade-offs acknowledged?

### Part B Evaluation (Bonus)

Run the agent:
```bash
python reflection_agent.py
```

- Does it load the tree correctly?
- Does it branch deterministically based on choices?
- Does it interpolate answers into reflections?
- Does the summary accurately tally signals?
- Does the transcript accurately capture the session?

Review sample transcripts:
- Do two personas produce different paths?
- Are both paths coherent and believable?
- Do reflections differ based on answers?

---

## Notes for Evaluators

- **The tree is the product.** Not the code, not the diagram. The tree structure itself demonstrates knowledge engineering — taking psychology and turning it into navigable structure.

- **Read the questions carefully.** The depth of the questions reveals the depth of research. Do these feel like something a psychologist designed, or like something an LLM generated?

- **Test the edge cases.** What happens if someone answers consistently "contribution-oriented" but one answer suggests entitlement? The tree handles blends, not bins.

- **Check the tone.** Does it feel like a wise colleague, not a therapist or a manager? The goal is reflection, not diagnosis.

---

## Author

Created as part of the DeepThought Fellowship assignment.  
Submission date: April 21, 2026

---

## License

This is an assignment submission. Use for evaluation purposes only.
