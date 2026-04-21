# Design Rationale: Daily Reflection Tree

## Overview
The Daily Reflection Tree is a 38-node deterministic agent that guides employees through a structured end-of-day reflection across three psychological axes: Locus of Control, Orientation (Contribution vs Entitlement), and Radius of Concern (Self-Centric vs Altrocentric). The design prioritizes honest self-discovery without judgment or moralizing.

## Why These Questions

### Axis 1: Locus of Control (Victim ↔ Victor)

**Source Psychology**: Rotter's locus of control theory (1954) and Dweck's growth mindset (2006).

**Opening question**: "If you had to pick one word for today?" (Productive/Mixed/Tough/Draining)
- Rather than asking directly "Did you have control?", I start with felt experience. This is how real people think — they first feel, then explain.
- The binary split (Productive vs Tough) allows natural branching without being judgmental.

**Follow-ups**:
- For positive framers: "What was YOUR role?" with options ranging from preparation to collaboration. This reinforces agency discovery in a frame where they already feel it.
- For negative framers: "What was your first instinct?" — crucial question because agency under stress is where the real insight lives. When things are easy, anyone feels in control. When things are hard, that's when you see if someone's internal or external.

**Why not ask directly**: "Did you feel in control?" Because that's what every self-help book asks, and people game the answer. By asking about their role in good outcomes and their instincts in hard moments, I'm getting at the actual *behavior* — which reveals the locus.

### Axis 2: Orientation (Contribution ↔ Entitlement)

**Source Psychology**: Organizational Citizenship Behavior (Organ, 1988) and Psychological Entitlement (Campbell et al., 2004).

**Key insight**: Entitlement is invisible to those who feel it. You can't ask "Were you entitled today?" — people will say no. So I ask about *moments* instead.

**Opening question**: "Think about one meaningful interaction..." — specifically asking for one moment, not a summary. This anchors people in reality, not abstraction.

**Branching logic**:
- If they describe helping/teaching → "What did you *feel*?" (not "What did you expect?"). Contribution often feels simple and forgotten. Entitlement demands recognition.
- If they felt unrecognized → "Where did you focus?" — watching whether they turn inward (self-examination) or outward (blame).

**Why not ask directly**: "Did you focus on what you gave or what you got?" Because that's backwards. They don't think in those buckets yet. I have to show them the difference through questions that reveal where their *actual* attention went.

### Axis 3: Radius of Concern (Self-Centric ↔ Altrocentric)

**Source Psychology**: Maslow's self-transcendence (1969) and Batson's perspective-taking (2011).

**Opening question**: "When you think about today's biggest challenge or win, whose world comes to mind first?" — progresses from "my world" → "our world" → "someone struggling" → "who we serve".
- This is not a hierarchy of better/worse. It's a spectrum of *radius*. Answering "my own" isn't wrong; it's just a narrower frame.

**Follow-ups ask about the *feeling***: 
- For self-focused: What happens when you focus only on yourself? (Watches for anxiety, isolation, volatility.)
- For other-focused: What shifts when you think about others? (Watches for meaning-making, energy, but also acknowledges burden.)

**Why this progression**: Maslow's peak experience isn't self-actualization — it's self-transcendence. But you can't guilt someone into it. The tree shows them the *cost* of narrow focus and the *benefit* of wide focus, without judgment.

## Branching Design Decisions

### Decision Nodes as Routers
I used decision nodes as invisible routers, not user-facing choices. This keeps the conversation flowing naturally without making the tree visible. The employee sees questions and reflections; the routing happens silently.

**Example**: A1_DECISION routes based on answer to A1_OPEN:
```
answer=Productive|Mixed → asks what made good things happen
answer=Tough|Draining → asks how they responded under stress
```

### Reflection Nodes as Reframes
After each axis, a reflection node doesn't judge — it *reframes*. For example:
- Internal locus reflection**: "You stayed in the driver's seat" — affirming agency even if it was imperfect.
- **External locus reflection**: "A tough day pulls attention outward... but somewhere you made a call" — validating difficulty while pointing to choice.

### Branching Convergence
Multiple paths converge to single nodes (e.g., all three Axis 1 reflections → BRIDGE_1_2). This ensures every conversation has the same flow and pacing, but personalized based on their answers.

### Signals for Aggregation
Each reflection node emits signals (axis1:internal, axis2:contribution, etc.). The agent tallies these. If someone gets multiple internal signals and one external, they're definitely "internal-leaning" — but not purely internal. The summary acknowledges the nuance.

## Trade-offs Made

1. **Fixed options over free text**: Required careful design of options that genuinely capture spectrum without leading. Risk: options might not fit someone's experience. Benefit: no ambiguity, fully deterministic.

2. **Sequence (Axis 1→2→3) vs parallel**: Could ask all three axes in any order, but sequence matters. Recognizing agency (Axis 1) makes it possible to ask about contribution (Axis 2). Knowing both helps contextualize radius (Axis 3) — it's easier to think about others once you see your own role.

3. **No scoring or "type" label**: Could bucket people into Victim/Victor, Contributor/Entitled, etc. Found it more humane to show them the blend and let them notice the pattern. Avoids the box.

4. **Reflection over advice**: The tree doesn't say "You should think about others more." It says "Notice what happens when you do." Shows result, not prescription.

## Psychological Grounding

**Locus of Control**: Questions surface whether employees see themselves as agents or reactors. Research (Rotter, Dweck) shows internal locus predicts resilience and learning. External can feel like relief ("It's not my fault") but also disempowerment.

**Contribution vs Entitlement**: Organ's work shows OCB (going beyond formal role) drives team performance. Campbell's entitlement research shows entitled employees are less satisfied despite expecting more. Questions probe actual behavior, not belief.

**Radius of Concern**: Maslow's transcendence and Batson's empathy research show that meaning and well-being increase when focus widens beyond self. But this isn't guilt — it's "the obstacle is the way." Serving others solves the stuck feeling.

## What I'd Improve With More Time

1. **Deeper follow-ups**: Could add a second layer of branching within Axis 2/3 for richer exploration.

2. **Longitudinal tracking**: Flag users who trend heavily external/entitled/self-centric and suggest deeper reflection. (But this risks prescriptiveness.)

3. **Day-of context**: Ask "What kind of day was it?" (meeting-heavy, crisis, creative, slow) and adapt question language. E.g., "in a meeting-heavy day, did you help someone?" vs "in a creative day, did you ship something you were proud of?"

4. **Weighted signals**: Some answers should count more. Asking for help (vulnerability) might indicate more growth than prepared work. Could add weights, but adds complexity.

5. **Reflection timing**: Add micro-pauses between sections. The tree auto-advances, but real reflection needs silence. Could insert wait-points.

6. **Tone variation**: Each persona (internal/external, etc.) could get subtly different language in reflections. Internal locus responders might respond better to "You drove this", external responders to "You navigated circumstances skillfully."

## Testing & Iteration

The questions have been tested against personas:
- **Victim persona**: Answers about tough day, being stuck, feeling unrecognized, focusing on self. Tree routes to reflections that gently highlight where they had choice.
- **Victor persona**: Productive day, took initiative, helped others, thinks about team. Tree affirms agency and contribution.
- **Entitlement persona**: Feels overlooked, focuses on what they're not getting. Tree surfaces the cost of that focus.

Each persona gets a different path but the same non-judgmental tone.

---

**Final note**: The goal is not to change someone in 5 minutes. It's to make them *notice* — agency, contribution, impact on others. Noticing precedes change. This tree is built to surface, not to fix.
