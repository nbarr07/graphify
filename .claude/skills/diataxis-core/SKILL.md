---
name: diataxis-core
description: Load when writing any documentation. Provides Diataxis framework rules — every document must belong to exactly one of four quadrants. Apply quadrant discipline before writing any file.
---

## What Diataxis Is

Diataxis is a systematic approach to technical documentation that organises content around user needs rather than topics. It identifies four distinct needs and four corresponding documentation forms. Every document you write must belong to exactly one quadrant. Crossing or blurring quadrant boundaries is the most common cause of documentation problems.

---

## The Four Quadrants

### The Compass

Before writing any document, ask two questions:

1. Is the content oriented towards **action** (doing something) or **cognition** (knowing/understanding something)?
2. Does it serve **acquisition** (the user is learning/studying) or **application** (the user is working)?

These two axes produce four quadrants:

```
                    ACTION
                      │
        TUTORIAL      │      HOW-TO GUIDE
     (learn by doing) │   (accomplish a task)
                      │
ACQUISITION ──────────┼────────────── APPLICATION
                      │
      EXPLANATION     │      REFERENCE
  (understand why)    │   (consult the facts)
                      │
                   COGNITION
```

---

## Quadrant Rules

### Tutorial — learning-oriented

**User need**: The user is a learner. They want to acquire skills and confidence through a guided experience.

**Your obligation**: Provide a successful learning experience. The learner's success is your responsibility.

**Do:**
- Guide the learner through a practical activity towards an achievable goal
- Ensure every step produces the result you promise — a learner who follows your directions and gets unexpected results loses confidence
- Keep the tutorial in a controlled, predictable environment — set everything up in advance
- Focus only on what is needed to reach the conclusion — ignore interesting diversions
- Inspire confidence at every stage — layer successes, never overwhelm
- Use concrete, specific tools and examples — not general or abstract ones
- Tell the learner what they will achieve at the start, not what they will learn ("In this tutorial we will build..." not "In this tutorial you will learn...")

**Do not:**
- Explain why things work — keep explanation minimal and link out to explanation docs instead
- Provide reference material — keep the learner focused on doing
- Give options or alternatives — the path must be singular and safe
- Assume the learner already has competence — you are responsible for their success
- Conflate a tutorial with a how-to guide — a tutorial teaches, a how-to guide directs work

**Signals this is a tutorial:**
- "Getting started", "Quickstart", "Your first X", "Build a..."
- The user has never done this before
- The outcome is learning, not completing a task

---

### How-to Guide — task-oriented

**User need**: The user is already competent. They want to accomplish a specific, real-world task correctly.

**Your obligation**: Help the user get the job done safely and correctly.

**Do:**
- Address a specific, concrete goal ("How to configure X", "How to deploy Y", "How to migrate Z")
- Assume the user has the necessary competence — you are guiding, not teaching
- Allow the path to fork and overlap — real-world problems are not always linear
- Stay focused on the goal — every step must serve it
- Use conditional imperatives: "If you want X, do Y"
- Link to reference material for full details rather than including them inline

**Do not:**
- Teach — if the user needs to learn first, they need a tutorial
- Explain why — if context is needed, link to explanation docs
- Include every possible option — only what is needed for this goal
- Frame it around the tool rather than the user's goal ("Using the export function" is tool-focused; "How to export data to CSV" is goal-focused)
- Confuse scope — "How to build a web application" is not a how-to guide; it is too open-ended to be a specific goal

**Signals this is a how-to guide:**
- "How to...", "Deploying...", "Configuring...", "Troubleshooting..."
- The user has a specific task to complete
- The user already knows how to use the product

---

### Reference — information-oriented

**User need**: The user is working and needs accurate, reliable facts to do their job correctly.

**Your obligation**: Describe the machinery accurately, completely, and neutrally. One hardly reads reference — one consults it.

**Do:**
- Describe the product as it is — APIs, functions, configuration options, CLI commands, data fields
- Mirror the structure of the product in the structure of the documentation — if a method belongs to a class, show that relationship
- Be austere and consistent — standard patterns allow users to navigate reference efficiently
- Provide examples only to illustrate, not to instruct
- Be wholly authoritative — no ambiguity, no doubt

**Do not:**
- Include instructions or steps — link to how-to guides instead
- Explain why things are the way they are — link to explanation docs instead
- Express opinions or perspectives
- Write in a narrative style — reference is consulted, not read
- Introduce unnecessary variety in structure — consistency is what makes reference usable

**Signals this is reference:**
- API documentation, CLI reference, configuration options, data dictionaries, glossaries
- The user needs to look something up while working
- The content describes the product, not how to use it

---

### Explanation — understanding-oriented

**User need**: The user wants to understand. They are studying, not working. They want context, background, and the bigger picture.

**Your obligation**: Illuminate the topic. Join things together. Help the user understand why.

**Do:**
- Take a higher, wider perspective than other documentation types
- Explain design decisions, historical reasons, technical constraints
- Consider alternatives and counter-examples — explanation can and should offer perspectives
- Circle around the subject and approach it from different angles
- Draw implications and make connections between concepts
- Use titles that can take the word "About" in front of them: "About authentication", "About the deployment model"

**Do not:**
- Include instructions or steps — those belong in tutorials or how-to guides
- Describe the machinery in detail — that belongs in reference
- Make it so specific that it only serves one task
- Pad tutorials with explanation — a brief inline note and a link out is enough
- Confuse explanation with reference — explanation illuminates, reference describes

**Signals this is explanation:**
- "About...", "Understanding...", "Architecture", "Why...", "Background"
- The user wants to understand, not do
- The content makes sense to read away from the product itself

---

## Quadrant Purity

Each document serves one quadrant and one quadrant only. The most common violations are:

| Violation | Problem | Fix |
|-----------|---------|-----|
| Tutorial that explains why | Breaks the learner's focus | Replace with a one-line note and link to explanation |
| How-to guide that teaches | Assumes the user needs to learn | Split into a tutorial and a separate how-to |
| Reference that instructs | Pollutes factual lookup with procedure | Move steps to a how-to guide |
| Explanation that includes steps | Confuses understanding with doing | Move steps to a tutorial or how-to guide |

If you find yourself unable to keep a document in one quadrant, that is a signal the document needs to be split into two separate documents.

Do not create empty quadrant folders or placeholder files. Structure emerges from content — only create a file when you have real content to put in it.

---

## The README Exception

READMEs sit outside the four quadrants. Their job is to orient a first-time visitor and route them to the right quadrant. A README should be a brief explanation of what the project is and why it exists, with links into the structured documentation. It is a signpost, not a documentation type.
