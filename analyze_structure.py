#!/usr/bin/env python3
"""
Comprehensive structure and mechanics analysis of David Knott's blog posts.
"""

import os
import re
from pathlib import Path
from collections import Counter, defaultdict
import json

# Blog directory
BLOG_DIR = Path("/Users/cns/httpdocs/dkblogs")

def get_blog_posts():
    """Get all blog post files, excluding backups."""
    posts = []
    for md_file in sorted(BLOG_DIR.glob("*.md")):
        if "_backup" not in str(md_file):
            posts.append(md_file)
    return posts

def read_post(filepath):
    """Read a blog post file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def get_first_sentences(content, n=2):
    """Extract first n sentences from content."""
    # Remove markdown formatting for sentence extraction
    text = content.strip()
    # Split by sentence endings
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences[:n]

def categorize_opening(first_sentence):
    """Categorize the opening type of a post."""
    sentence = first_sentence.strip()

    # Question - starts with question word or ends with ?
    if sentence.endswith('?') or re.match(r'^(What|How|Why|When|Where|Who|Do|Does|Did|Can|Could|Would|Should|Is|Are|Will|Have|Has)', sentence):
        return 'question'

    # Confession/admission - contains "I" statements about personal state
    if re.match(r'^I (am|was|have|had|\'m|\'ve|don\'t|didn\'t|can\'t)', sentence):
        return 'confession'

    # Fact - contains specific dates, numbers, or definitive statements
    if re.search(r'\b(19|20)\d{2}\b|^\w+\s+(is|are|was|were)\s+', sentence):
        return 'fact'

    # Anecdote - narrative markers
    if re.match(r'^(Last|Yesterday|Recently|A few|The other|Once|One)', sentence):
        return 'anecdote'

    # Default to statement
    return 'statement'

def extract_bold_headers(content):
    """Extract bold headers from content."""
    # Match **text** pattern
    headers = re.findall(r'\*\*(.*?)\*\*', content)
    return headers

def count_h2_h3(content):
    """Count H2 and H3 markdown headers."""
    h2_count = len(re.findall(r'^## [^#]', content, re.MULTILINE))
    h3_count = len(re.findall(r'^### [^#]', content, re.MULTILINE))
    return h2_count, h3_count

def analyze_paragraphs(content):
    """Analyze paragraph structure."""
    # Split into paragraphs (double newline)
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

    paragraph_data = []
    for para in paragraphs:
        # Count sentences in paragraph
        sentences = re.split(r'(?<=[.!?])\s+', para)
        sentences = [s for s in sentences if s.strip()]

        paragraph_data.append({
            'sentence_count': len(sentences),
            'char_length': len(para),
            'starts_with': para[:50] if len(para) >= 50 else para
        })

    return paragraph_data

def extract_closing_disclaimer(content):
    """Extract the closing disclaimer and paragraph before it."""
    lines = content.split('\n')

    # Look for disclaimer patterns
    disclaimer_patterns = [
        r'These are my personal views',
        r'This article is my personal view',
        r'The views expressed',
        r'personal view',
        r'personal opinion'
    ]

    disclaimer_line = None
    for i, line in enumerate(lines):
        for pattern in disclaimer_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                disclaimer_line = i
                break
        if disclaimer_line:
            break

    if disclaimer_line:
        # Get paragraph before disclaimer
        before_disclaimer = '\n'.join(lines[:disclaimer_line]).strip()
        last_para = before_disclaimer.split('\n\n')[-1] if before_disclaimer else ""
        disclaimer_text = '\n'.join(lines[disclaimer_line:]).strip()
        return last_para, disclaimer_text

    return None, None

def count_formatting(content):
    """Count various formatting uses."""
    bold_count = len(re.findall(r'\*\*(.*?)\*\*', content))
    italic_count = len(re.findall(r'\*(.*?)\*', content)) - bold_count * 2  # Exclude ** matches
    link_count = len(re.findall(r'\[.*?\]\(.*?\)', content))
    paren_count = len(re.findall(r'\([^)]+\)', content)) - link_count  # Exclude link parens
    emdash_count = len(re.findall(r'—', content))
    bullet_count = len(re.findall(r'^\s*[-*+]\s', content, re.MULTILINE))
    number_count = len(re.findall(r'^\s*\d+\.\s', content, re.MULTILINE))

    return {
        'bold': bold_count,
        'italic': italic_count,
        'links': link_count,
        'parentheticals': paren_count,
        'em_dashes': emdash_count,
        'bullet_lists': bullet_count,
        'numbered_lists': number_count
    }

def count_words(content):
    """Count words in content."""
    # Remove markdown formatting
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)  # Links
    text = re.sub(r'[*_#]', '', text)  # Markdown chars
    words = text.split()
    return len(words)

def main():
    posts = get_blog_posts()
    print(f"Analyzing {len(posts)} blog posts...\n")

    # Data collection
    all_data = {
        'openings': [],
        'structures': [],
        'paragraphs': [],
        'closings': [],
        'formatting': [],
        'lengths': []
    }

    opening_types = Counter()
    first_sentence_lengths = []

    for post_path in posts:
        content = read_post(post_path)
        post_name = post_path.stem

        # Opening analysis
        first_sents = get_first_sentences(content, 2)
        if first_sents:
            first_sent = first_sents[0]
            opening_type = categorize_opening(first_sent)
            opening_types[opening_type] += 1
            first_sentence_lengths.append(len(first_sent))

            all_data['openings'].append({
                'post': post_name,
                'type': opening_type,
                'first_sentence': first_sent,
                'second_sentence': first_sents[1] if len(first_sents) > 1 else ''
            })

        # Structure analysis
        bold_headers = extract_bold_headers(content)
        h2_count, h3_count = count_h2_h3(content)

        all_data['structures'].append({
            'post': post_name,
            'has_bold_headers': len(bold_headers) > 0,
            'bold_header_count': len(bold_headers),
            'bold_headers': bold_headers,
            'h2_count': h2_count,
            'h3_count': h3_count
        })

        # Paragraph analysis
        para_data = analyze_paragraphs(content)
        all_data['paragraphs'].append({
            'post': post_name,
            'paragraph_count': len(para_data),
            'paragraphs': para_data
        })

        # Closing analysis
        last_para, disclaimer = extract_closing_disclaimer(content)
        all_data['closings'].append({
            'post': post_name,
            'last_paragraph': last_para,
            'disclaimer': disclaimer
        })

        # Formatting analysis
        formatting = count_formatting(content)
        all_data['formatting'].append({
            'post': post_name,
            **formatting
        })

        # Length analysis
        word_count = count_words(content)
        all_data['lengths'].append({
            'post': post_name,
            'word_count': word_count
        })

    # Save raw data
    with open('/Users/cns/httpdocs/dkblogs/structure_analysis.json', 'w') as f:
        json.dump(all_data, f, indent=2)

    # Generate summary report
    report = []
    report.append("=" * 80)
    report.append("DAVID KNOTT BLOG STRUCTURE & MECHANICS ANALYSIS")
    report.append("=" * 80)
    report.append("")

    # 1. OPENING PATTERNS
    report.append("1. OPENING PATTERNS")
    report.append("-" * 80)
    total_posts = len(posts)
    for opening_type, count in opening_types.most_common():
        pct = (count / total_posts) * 100
        report.append(f"  {opening_type.upper()}: {count} posts ({pct:.1f}%)")

    report.append(f"\nFirst sentence length: {sum(first_sentence_lengths)/len(first_sentence_lengths):.1f} chars (avg)")
    report.append(f"  Min: {min(first_sentence_lengths)} chars")
    report.append(f"  Max: {max(first_sentence_lengths)} chars")

    report.append("\nSample openings by type:")
    for opening_type in ['question', 'confession', 'fact', 'anecdote', 'statement']:
        samples = [o for o in all_data['openings'] if o['type'] == opening_type][:3]
        if samples:
            report.append(f"\n  {opening_type.upper()}:")
            for s in samples:
                report.append(f"    - {s['first_sentence'][:100]}...")

    # 2. SECTION ORGANIZATION
    report.append("\n\n2. SECTION ORGANIZATION")
    report.append("-" * 80)

    posts_with_bold = sum(1 for s in all_data['structures'] if s['has_bold_headers'])
    report.append(f"Posts with bold headers: {posts_with_bold}/{total_posts} ({posts_with_bold/total_posts*100:.1f}%)")

    bold_header_counts = [s['bold_header_count'] for s in all_data['structures'] if s['bold_header_count'] > 0]
    if bold_header_counts:
        report.append(f"Average bold headers per structured post: {sum(bold_header_counts)/len(bold_header_counts):.1f}")

    h2_total = sum(s['h2_count'] for s in all_data['structures'])
    h3_total = sum(s['h3_count'] for s in all_data['structures'])
    report.append(f"H2 headers found: {h2_total}")
    report.append(f"H3 headers found: {h3_total}")

    # Analyze header naming
    all_headers = []
    for s in all_data['structures']:
        all_headers.extend(s['bold_headers'])

    report.append(f"\nTotal bold headers analyzed: {len(all_headers)}")
    if all_headers:
        # Sample headers
        report.append("\nSample bold headers:")
        for h in all_headers[:20]:
            report.append(f"  - {h}")

    # 3. PARAGRAPH ARCHITECTURE
    report.append("\n\n3. PARAGRAPH ARCHITECTURE")
    report.append("-" * 80)

    all_para_counts = []
    single_sentence_paras = 0
    total_paras = 0

    for p_data in all_data['paragraphs']:
        all_para_counts.append(p_data['paragraph_count'])
        for para in p_data['paragraphs']:
            total_paras += 1
            if para['sentence_count'] == 1:
                single_sentence_paras += 1

    report.append(f"Average paragraphs per post: {sum(all_para_counts)/len(all_para_counts):.1f}")
    report.append(f"Single-sentence paragraphs: {single_sentence_paras}/{total_paras} ({single_sentence_paras/total_paras*100:.1f}%)")

    # 4. CLOSING PATTERNS
    report.append("\n\n4. CLOSING PATTERNS")
    report.append("-" * 80)

    disclaimers_found = sum(1 for c in all_data['closings'] if c['disclaimer'])
    report.append(f"Posts with disclaimer: {disclaimers_found}/{total_posts}")

    # Show disclaimer variants
    unique_disclaimers = set()
    for c in all_data['closings']:
        if c['disclaimer']:
            unique_disclaimers.add(c['disclaimer'][:100])

    report.append(f"\nUnique disclaimer variants: {len(unique_disclaimers)}")

    # 5. FORMATTING CONVENTIONS
    report.append("\n\n5. FORMATTING CONVENTIONS")
    report.append("-" * 80)

    formatting_totals = defaultdict(int)
    for f in all_data['formatting']:
        for key, val in f.items():
            if key != 'post':
                formatting_totals[key] += val

    for key, total in sorted(formatting_totals.items()):
        avg = total / total_posts
        report.append(f"{key}: {total} total, {avg:.1f} per post (avg)")

    # 6. LENGTH ANALYSIS
    report.append("\n\n6. LENGTH ANALYSIS")
    report.append("-" * 80)

    word_counts = [l['word_count'] for l in all_data['lengths']]
    report.append(f"Average word count: {sum(word_counts)/len(word_counts):.0f}")
    report.append(f"Median word count: {sorted(word_counts)[len(word_counts)//2]}")
    report.append(f"Min word count: {min(word_counts)}")
    report.append(f"Max word count: {max(word_counts)}")

    # Find shortest and longest
    shortest = min(all_data['lengths'], key=lambda x: x['word_count'])
    longest = max(all_data['lengths'], key=lambda x: x['word_count'])

    report.append(f"\nShortest post: {shortest['post']} ({shortest['word_count']} words)")
    report.append(f"Longest post: {longest['post']} ({longest['word_count']} words)")

    # Word count distribution
    ranges = [(0, 500), (500, 750), (750, 1000), (1000, 1250), (1250, 1500), (1500, 2000), (2000, 10000)]
    report.append("\nWord count distribution:")
    for low, high in ranges:
        count = sum(1 for wc in word_counts if low <= wc < high)
        pct = (count / total_posts) * 100
        report.append(f"  {low}-{high}: {count} posts ({pct:.1f}%)")

    report.append("\n" + "=" * 80)

    # Write report
    report_text = '\n'.join(report)
    with open('/Users/cns/httpdocs/dkblogs/structure_report.txt', 'w') as f:
        f.write(report_text)

    print(report_text)
    print("\n\nDetailed data saved to: structure_analysis.json")
    print("Summary report saved to: structure_report.txt")

if __name__ == '__main__':
    main()
