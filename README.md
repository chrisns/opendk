# OpenDK: David Knott Writing Style Analysis

A comprehensive linguistic and rhetorical analysis of [David Knott's LinkedIn newsletter](https://www.linkedin.com/newsletters/6694123842199154688/), spanning 180 posts from June 2022 to December 2025.

## Usage

This style guide is designed to be used with AI assistants (Claude, ChatGPT, etc.) to generate new articles in David's voice.

### Basic prompt

```
Based only on @style.md write a new original article in David's voice on a topic that he would write about
```

### With a specific topic

```
Based only on @style.md write a new original article in David's voice about technical debt
```

### For editing/feedback

```
Using @style.md as a reference, review this draft and suggest edits to make it sound more like David's writing style
```

The `style.md` file contains all the patterns, ratios, and examples needed for an AI to replicate the voice accurately.

---

## Purpose

This repository contains the tools and outputs from an in-depth analysis of David Knott's writing style. The goal is to capture the distinctive voice, structure, and rhetorical patterns that make his enterprise technology writing recognisable and effective.

David writes about technology leadership, legacy systems, cloud computing, AI, and the human factors in enterprise technology. His style is characterised by collaborative framing, extended analogies, and intellectual humility.

## Key Findings

### Voice Profile

David writes like a **thoughtful colleague thinking out loud with you**, not an expert lecturing down at you.

| Attribute | Ratio |
|-----------|-------|
| "We" vs "I" | 1.6:1 (collaborative framing) |
| Hedging vs Assertion | 8.67:1 (intellectual humility) |
| "I think" vs "I believe" | 1.85:1 (exploratory over conviction) |

### Structure Patterns

- **79%** of posts use flowing prose without section headers
- **29%** of paragraphs are single sentences (creates rhythm)
- **75%** of openings are fact-based scenarios (not questions)
- **99.4%** end with the disclaimer: *"(Views in this article are my own.)"*
- **Sweet spot**: 750-1,000 words (80% of posts)

### Signature Elements

- British English throughout (organisation, realise, behaviour)
- Extended analogies from space exploration, food, classical philosophy
- The "However," pivot (appears in 87% of posts)
- Three-part frameworks with memorable names
- Parenthetical asides (~4 per post)

## Repository Contents

### Style Guides

| File | Description |
|------|-------------|
| `style.md` | **Master style guide** - comprehensive reference for replicating David's voice |
| `VOICE_QUICK_REFERENCE.md` | Quick lookup card for voice patterns |
| `VOICE_STYLE_GUIDE_COMPREHENSIVE.md` | Deep dive into pronoun usage and tone |
| `STYLE_GUIDE_STRUCTURE_MECHANICS.md` | Formatting, paragraphs, and organisation |
| `RHETORICAL_ARGUMENT_PATTERNS_STYLE_GUIDE.md` | How arguments are constructed |

### Analysis Reports

| File | Description |
|------|-------------|
| `ANALYSIS_SUMMARY.md` | High-level findings across all posts |
| `RHETORIC_ANALYSIS_SUMMARY.md` | Rhetorical device usage patterns |
| `THEMATIC_ANALYSIS.md` | Topic frequency and recurring themes |
| `EXAMPLES_ANNOTATED.md` | Annotated excerpts showing patterns in action |
| `ARGUMENT_FLOW_EXAMPLES.md` | How arguments develop paragraph by paragraph |

### Analysis Tools

| File | Description |
|------|-------------|
| `analyze_structure.py` | Paragraph and formatting analysis |
| `analyze_structure_v2.py` | Enhanced structure metrics |
| `analyze_rhetoric.py` | Rhetorical pattern detection |
| `voice_analysis.py` | Pronoun and hedging analysis |
| `voice_analysis_deep.py` | Extended voice pattern analysis |
| `voice_analysis_examples.py` | Extract representative examples |

### Raw Data

| File | Description |
|------|-------------|
| `structure_analysis.json` | Structured data from analysis |
| `rhetoric_analysis.json` | Rhetorical patterns data |
| `*_report.txt` | Human-readable analysis outputs |

## The Formula

```
Question Hook (in title) → Concrete Opening → Acknowledge Conventional Wisdom
→ "However, I believe..." → Three-Part Framework → Develop with Analogies
→ Address Counterarguments → Synthesize → Measured Action + Humility → Disclaimer
```

## Quick Voice Checklist

Before writing in David's style, verify:

- [ ] British spellings throughout
- [ ] "We" appears more than "I"
- [ ] At least one "However," pivot
- [ ] Extended analogy from a concrete domain
- [ ] Self-deprecating admission included
- [ ] No exclamation marks
- [ ] Ends with disclaimer
- [ ] 750-1,000 words

## Licence

This analysis is provided for educational and research purposes. The original blog posts remain the intellectual property of David Knott.
