#!/usr/bin/env python3
"""
Analyze David Knott's blog posts for rhetorical and argument patterns
"""

import re
import os
from pathlib import Path
from collections import defaultdict, Counter
import json

BLOG_DIR = "/Users/cns/httpdocs/dkblogs"

def get_blog_posts():
    """Get all blog post files, excluding backups"""
    posts = []
    for file in sorted(Path(BLOG_DIR).glob("*.md")):
        if "_backup" not in str(file):
            posts.append(file)
    return posts

def read_post(filepath):
    """Read a blog post file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def analyze_questions(content):
    """Analyze question usage in a post"""
    lines = content.split('\n')

    # Count total question marks
    question_count = content.count('?')

    # Find opening questions (first paragraph with ?)
    opening_question = None
    in_content = False
    for i, line in enumerate(lines):
        if line.strip().startswith('---'):
            in_content = not in_content
            continue
        if in_content and '?' in line and line.strip():
            opening_question = line.strip()
            break

    # Find all questions
    questions = []
    for line in lines:
        if '?' in line:
            # Extract sentences ending with ?
            sents = re.findall(r'[^.!?]*\?', line)
            questions.extend([s.strip() for s in sents if s.strip()])

    return {
        'count': question_count,
        'opening': opening_question,
        'all_questions': questions
    }

def analyze_rule_of_three(content):
    """Analyze rule of three patterns"""
    patterns = {
        'first_second_third': [],
        'triadic_lists': [],
        'three_part_structures': []
    }

    # Pattern 1: First, Second, Third
    first_second = re.findall(r'(First[,:].*?(?:Second[,:].*?(?:Third[,:].*?)?)?)', content, re.IGNORECASE | re.DOTALL)
    patterns['first_second_third'] = first_second[:3] if first_second else []

    # Pattern 2: X, Y, and Z (triadic lists)
    triads = re.findall(r'\b(\w+(?:\s+\w+)?),\s+(\w+(?:\s+\w+)?),?\s+and\s+(\w+(?:\s+\w+)?)\b', content)
    patterns['triadic_lists'] = triads[:10] if triads else []

    # Pattern 3: Numbered lists (1., 2., 3.)
    numbered = re.findall(r'(1\..*?2\..*?3\.)', content, re.DOTALL)
    patterns['three_part_structures'] = numbered[:3] if numbered else []

    return patterns

def analyze_counterarguments(content):
    """Analyze counterargument patterns"""
    patterns = {
        'however': [],
        'but': [],
        'and_yet': [],
        'this_is_not_to_say': [],
        'on_the_other_hand': []
    }

    # Find sentences with counterargument markers
    sentences = re.split(r'[.!?]\s+', content)

    for sent in sentences:
        sent_lower = sent.lower()
        if sent_lower.startswith('however'):
            patterns['however'].append(sent.strip()[:200])
        if sent_lower.startswith('but ') or ' but ' in sent_lower:
            patterns['but'].append(sent.strip()[:200])
        if 'and yet' in sent_lower:
            patterns['and_yet'].append(sent.strip()[:200])
        if 'this is not to say' in sent_lower:
            patterns['this_is_not_to_say'].append(sent.strip()[:200])
        if 'on the other hand' in sent_lower:
            patterns['on_the_other_hand'].append(sent.strip()[:200])

    return {k: v[:3] for k, v in patterns.items()}  # Limit to 3 examples each

def analyze_evidence(content):
    """Analyze evidence integration patterns"""
    evidence = {
        'personal_experience': [],
        'external_references': [],
        'analogies': [],
        'historical_examples': []
    }

    # Personal experience markers
    personal_markers = [
        r"In my (?:career|experience|view|opinion)",
        r"I have (?:seen|found|noticed|observed)",
        r"I've (?:seen|found|noticed|observed)",
        r"When I (?:was|worked|started)"
    ]

    for marker in personal_markers:
        matches = re.findall(rf'{marker}[^.!?]*[.!?]', content, re.IGNORECASE)
        evidence['personal_experience'].extend(matches[:2])

    # External references (books, articles, podcasts)
    ref_markers = [
        r'(?:book|article|podcast|paper|study)(?:\s+\w+){0,5}(?:called|titled|named)',
        r'(?:According to|As per|In)\s+[\w\s]+(?:wrote|said|argued)',
        r'\[.*?\]\(http'  # Markdown links
    ]

    for marker in ref_markers:
        matches = re.findall(rf'{marker}[^.!?]*[.!?]', content, re.IGNORECASE)
        evidence['external_references'].extend(matches[:2])

    # Analogies (like, as if, similar to, just as)
    analogy_markers = [
        r'(?:is|are)\s+like\s+\w+',
        r'(?:is|are)\s+similar to',
        r'just as\s+\w+',
        r'imagine\s+\w+'
    ]

    for marker in analogy_markers:
        matches = re.findall(rf'{marker}[^.!?]*[.!?]', content, re.IGNORECASE)
        evidence['analogies'].extend(matches[:2])

    return {k: v[:5] for k, v in evidence.items()}

def analyze_conclusions(content):
    """Analyze how posts conclude"""
    lines = content.split('\n')

    # Get last 5 non-empty lines (excluding frontmatter)
    content_lines = [l for l in lines if l.strip() and not l.startswith('---')]
    conclusion = '\n'.join(content_lines[-10:]) if len(content_lines) >= 10 else '\n'.join(content_lines[-5:])

    patterns = {
        'action_oriented': bool(re.search(r'\b(?:we should|we can|we must|we need to|let us|let\'s)\b', conclusion, re.IGNORECASE)),
        'humility_markers': bool(re.search(r'\b(?:perhaps|maybe|might|could|possibly|may be)\b', conclusion, re.IGNORECASE)),
        'measured': bool(re.search(r'\b(?:careful|consider|think about|reflect|remember)\b', conclusion, re.IGNORECASE)),
        'conclusion_text': conclusion[-500:] if len(conclusion) > 500 else conclusion
    }

    return patterns

def analyze_repetition(content):
    """Analyze repetition and emphasis patterns"""
    lines = content.split('\n')
    sentences = re.split(r'[.!?]\s+', content)

    # Anaphora - sentences starting with the same words
    sentence_starts = []
    for sent in sentences:
        words = sent.strip().split()
        if len(words) >= 3:
            sentence_starts.append(' '.join(words[:2]))

    start_counts = Counter(sentence_starts)
    repeated_starts = [(start, count) for start, count in start_counts.most_common(10) if count > 2]

    # "If your motivation is" pattern
    motivation_pattern = re.findall(r'If your.*?(?:is|was|are|were).*?[.!?]', content, re.IGNORECASE)

    return {
        'repeated_sentence_starts': repeated_starts,
        'motivation_patterns': motivation_pattern[:5]
    }

def extract_structure(content):
    """Extract post structure"""
    lines = content.split('\n')

    # Remove frontmatter
    content_lines = []
    in_frontmatter = False
    frontmatter_count = 0

    for line in lines:
        if line.strip() == '---':
            frontmatter_count += 1
            if frontmatter_count == 2:
                in_frontmatter = False
                continue
            else:
                in_frontmatter = True
                continue
        if not in_frontmatter:
            content_lines.append(line)

    content_text = '\n'.join(content_lines)

    # Look for sections
    sections = []
    paragraphs = [p.strip() for p in content_text.split('\n\n') if p.strip()]

    structure = {
        'paragraph_count': len(paragraphs),
        'opening': paragraphs[0][:200] if paragraphs else '',
        'closing': paragraphs[-1][:200] if paragraphs else '',
        'has_disclaimer': bool(re.search(r'\b(?:disclaimer|caveat|note:)\b', content_text, re.IGNORECASE))
    }

    return structure

def main():
    posts = get_blog_posts()
    print(f"Analyzing {len(posts)} blog posts...\n")

    all_analysis = {
        'total_posts': len(posts),
        'question_stats': {
            'total_questions': 0,
            'avg_per_post': 0,
            'posts_with_title_questions': 0,
            'opening_questions': [],
            'example_questions': []
        },
        'rule_of_three': {
            'posts_with_first_second_third': 0,
            'posts_with_triads': 0,
            'examples': []
        },
        'counterarguments': {
            'however_count': 0,
            'but_count': 0,
            'and_yet_count': 0,
            'examples': []
        },
        'evidence': {
            'personal_experience_count': 0,
            'external_refs_count': 0,
            'analogy_count': 0,
            'examples': []
        },
        'conclusions': {
            'action_oriented': 0,
            'with_humility': 0,
            'measured': 0,
            'examples': []
        },
        'repetition': {
            'repeated_starts': [],
            'examples': []
        },
        'structure': {
            'avg_paragraphs': 0,
            'posts_with_disclaimers': 0
        }
    }

    total_questions = 0
    total_paragraphs = 0

    for i, post in enumerate(posts):
        content = read_post(post)
        filename = post.name

        # Questions
        q_analysis = analyze_questions(content)
        total_questions += q_analysis['count']
        if '?' in post.name:
            all_analysis['question_stats']['posts_with_title_questions'] += 1
        if q_analysis['opening'] and len(all_analysis['question_stats']['opening_questions']) < 20:
            all_analysis['question_stats']['opening_questions'].append({
                'post': filename,
                'question': q_analysis['opening']
            })

        # Rule of three
        three_analysis = analyze_rule_of_three(content)
        if three_analysis['first_second_third']:
            all_analysis['rule_of_three']['posts_with_first_second_third'] += 1
        if three_analysis['triadic_lists']:
            all_analysis['rule_of_three']['posts_with_triads'] += 1
            if len(all_analysis['rule_of_three']['examples']) < 20:
                all_analysis['rule_of_three']['examples'].append({
                    'post': filename,
                    'triads': three_analysis['triadic_lists'][:3]
                })

        # Counterarguments
        counter_analysis = analyze_counterarguments(content)
        all_analysis['counterarguments']['however_count'] += len(counter_analysis['however'])
        all_analysis['counterarguments']['but_count'] += len(counter_analysis['but'])
        all_analysis['counterarguments']['and_yet_count'] += len(counter_analysis['and_yet'])
        if any(counter_analysis.values()) and len(all_analysis['counterarguments']['examples']) < 20:
            all_analysis['counterarguments']['examples'].append({
                'post': filename,
                'patterns': counter_analysis
            })

        # Evidence
        ev_analysis = analyze_evidence(content)
        all_analysis['evidence']['personal_experience_count'] += len(ev_analysis['personal_experience'])
        all_analysis['evidence']['external_refs_count'] += len(ev_analysis['external_references'])
        all_analysis['evidence']['analogy_count'] += len(ev_analysis['analogies'])
        if any(ev_analysis.values()) and len(all_analysis['evidence']['examples']) < 15:
            all_analysis['evidence']['examples'].append({
                'post': filename,
                'evidence': ev_analysis
            })

        # Conclusions
        conc_analysis = analyze_conclusions(content)
        if conc_analysis['action_oriented']:
            all_analysis['conclusions']['action_oriented'] += 1
        if conc_analysis['humility_markers']:
            all_analysis['conclusions']['with_humility'] += 1
        if conc_analysis['measured']:
            all_analysis['conclusions']['measured'] += 1
        if len(all_analysis['conclusions']['examples']) < 15:
            all_analysis['conclusions']['examples'].append({
                'post': filename,
                'patterns': {k: v for k, v in conc_analysis.items() if k != 'conclusion_text'},
                'text': conc_analysis['conclusion_text'][:300]
            })

        # Repetition
        rep_analysis = analyze_repetition(content)
        if rep_analysis['repeated_sentence_starts'] and len(all_analysis['repetition']['examples']) < 15:
            all_analysis['repetition']['examples'].append({
                'post': filename,
                'patterns': rep_analysis
            })

        # Structure
        struct_analysis = extract_structure(content)
        total_paragraphs += struct_analysis['paragraph_count']
        if struct_analysis['has_disclaimer']:
            all_analysis['structure']['posts_with_disclaimers'] += 1

        if (i + 1) % 50 == 0:
            print(f"Processed {i + 1} posts...")

    # Calculate averages
    all_analysis['question_stats']['total_questions'] = total_questions
    all_analysis['question_stats']['avg_per_post'] = round(total_questions / len(posts), 2)
    all_analysis['structure']['avg_paragraphs'] = round(total_paragraphs / len(posts), 2)

    # Save to JSON
    output_file = '/Users/cns/httpdocs/dkblogs/rhetoric_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_analysis, f, indent=2, ensure_ascii=False)

    print(f"\nAnalysis complete! Results saved to {output_file}")
    print(f"\nQuick Stats:")
    print(f"  Total questions: {total_questions}")
    print(f"  Avg questions per post: {all_analysis['question_stats']['avg_per_post']}")
    print(f"  Posts with title questions: {all_analysis['question_stats']['posts_with_title_questions']}")
    print(f"  Posts with 'First, Second, Third': {all_analysis['rule_of_three']['posts_with_first_second_third']}")
    print(f"  Posts with triadic lists: {all_analysis['rule_of_three']['posts_with_triads']}")
    print(f"  'However' usage: {all_analysis['counterarguments']['however_count']}")
    print(f"  Action-oriented conclusions: {all_analysis['conclusions']['action_oriented']}")
    print(f"  Avg paragraphs per post: {all_analysis['structure']['avg_paragraphs']}")

if __name__ == '__main__':
    main()
