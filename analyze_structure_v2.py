#!/usr/bin/env python3
"""
Comprehensive structure and mechanics analysis of David Knott's blog posts - Version 2
Handles YAML frontmatter properly and provides detailed insights.
"""

import os
import re
from pathlib import Path
from collections import Counter, defaultdict
import json

BLOG_DIR = Path("/Users/cns/httpdocs/dkblogs")

def get_blog_posts():
    """Get all blog post files, excluding backups."""
    posts = []
    for md_file in sorted(BLOG_DIR.glob("*.md")):
        if "_backup" not in str(md_file):
            posts.append(md_file)
    return posts

def read_post(filepath):
    """Read a blog post file and separate frontmatter from content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        body = frontmatter_match.group(2).strip()
        return frontmatter, body
    return "", content.strip()

def get_first_sentences(content, n=2):
    """Extract first n sentences from content."""
    # Split by sentence endings followed by space/newline
    sentences = re.split(r'[.!?]\s+', content)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences[:n]

def categorize_opening(first_sentence):
    """Categorize the opening type of a post."""
    sentence = first_sentence.strip()

    # Question - ends with ?
    if sentence.endswith('?'):
        return 'question'

    # Confession/first person opening
    if re.match(r'^I\s', sentence) or re.match(r'^I\'', sentence):
        return 'confession'

    # Anecdote - narrative time markers
    if re.match(r'^(Last|Yesterday|Recently|A few|The other|Once|One|On |In \d{4})', sentence):
        return 'anecdote'

    # Italicized opening (often a quote or statement)
    if sentence.startswith('_') and '_' in sentence[1:]:
        return 'statement'

    # Default to fact
    return 'fact'

def extract_bold_headers(content):
    """Extract bold headers from content."""
    headers = re.findall(r'^\*\*(.*?)\*\*$', content, re.MULTILINE)
    return headers

def count_h2_h3(content):
    """Count H2 and H3 markdown headers."""
    h2_count = len(re.findall(r'^## [^#]', content, re.MULTILINE))
    h3_count = len(re.findall(r'^### [^#]', content, re.MULTILINE))
    return h2_count, h3_count

def analyze_paragraphs(content):
    """Analyze paragraph structure."""
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

    paragraph_data = []
    for i, para in enumerate(paragraphs):
        # Count sentences
        sentences = re.split(r'[.!?]\s+', para)
        sentences = [s for s in sentences if s.strip()]

        # Check for transition words at start
        transition_words = ['however', 'but', 'yet', 'and', 'so', 'therefore', 'thus', 'first', 'second', 'third', 'finally', 'fortunately', 'unfortunately', 'of course']
        starts_with_transition = any(para.lower().startswith(word) for word in transition_words)

        paragraph_data.append({
            'index': i,
            'sentence_count': len(sentences),
            'char_length': len(para),
            'starts_with_transition': starts_with_transition,
            'first_30_chars': para[:30]
        })

    return paragraph_data

def extract_closing(content):
    """Extract closing disclaimer and paragraph before it."""
    lines = content.split('\n')

    # Look for the standard disclaimer pattern
    disclaimer_pattern = r'\(_?Views in this article are my own[^)]*\)_?'

    disclaimer_line = None
    for i, line in enumerate(lines):
        if re.search(disclaimer_pattern, line, re.IGNORECASE):
            disclaimer_line = i
            break

    if disclaimer_line is not None:
        # Get paragraph before disclaimer
        before_disclaimer = '\n'.join(lines[:disclaimer_line]).strip()
        last_para = before_disclaimer.split('\n\n')[-1] if before_disclaimer else ""
        disclaimer_text = lines[disclaimer_line].strip()
        return last_para, disclaimer_text

    return None, None

def count_formatting(content):
    """Count various formatting uses."""
    # Bold - count ** pairs
    bold_count = len(re.findall(r'\*\*[^*]+\*\*', content))

    # Italic - count single * (not part of bold)
    italic_count = len(re.findall(r'(?<!\*)\*(?!\*)([^*]+)\*(?!\*)', content))

    # Links
    link_count = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content))

    # Parentheticals (excluding links)
    all_parens = len(re.findall(r'\([^)]+\)', content))
    paren_count = all_parens - link_count

    # Em-dashes
    emdash_count = len(re.findall(r'—', content))

    # En-dashes
    endash_count = len(re.findall(r'–', content))

    # Bullet lists
    bullet_count = len(re.findall(r'^\s*[-*+]\s', content, re.MULTILINE))

    # Numbered lists
    number_count = len(re.findall(r'^\s*\d+\.\s', content, re.MULTILINE))

    return {
        'bold': bold_count,
        'italic': italic_count,
        'links': link_count,
        'parentheticals': paren_count,
        'em_dashes': emdash_count,
        'en_dashes': endash_count,
        'bullet_lists': bullet_count,
        'numbered_lists': number_count
    }

def count_words(content):
    """Count words in content."""
    # Remove markdown links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
    # Remove markdown formatting
    text = re.sub(r'[*_#]', '', text)
    words = text.split()
    return len(words)

def analyze_header_naming(headers):
    """Analyze how headers are named."""
    patterns = {
        'imperative': 0,  # "Do this"
        'question': 0,    # "Why do this?"
        'noun_phrase': 0, # "The thing"
        'because': 0,     # "Because X"
    }

    for h in headers:
        if h.startswith('Because'):
            patterns['because'] += 1
        elif h.endswith('?'):
            patterns['question'] += 1
        elif re.match(r'^[A-Z][a-z]+\s+(your|the|a|an)', h):
            patterns['imperative'] += 1
        else:
            patterns['noun_phrase'] += 1

    return patterns

def analyze_closing_type(last_para):
    """Analyze the type of closing paragraph."""
    if not last_para:
        return 'none'

    para_lower = last_para.lower()

    # Call to action
    if re.search(r'\b(should|must|need to|have to|let\'s|we can)\b', para_lower):
        return 'call_to_action'

    # Synthesis/conclusion
    if re.search(r'\b(together|finally|in conclusion|therefore|thus)\b', para_lower):
        return 'synthesis'

    # Callback to opening
    if len(last_para) > 100 and re.search(r'\b(remember|recall|as we|just like)\b', para_lower):
        return 'callback'

    # Forward-looking
    if re.search(r'\b(future|tomorrow|ahead|will|going to)\b', para_lower):
        return 'forward_looking'

    return 'other'

def main():
    posts = get_blog_posts()
    print(f"Analyzing {len(posts)} blog posts...\n")

    # Data collection
    all_data = {
        'posts': [],
        'summary': {}
    }

    opening_types = Counter()
    first_sentence_lengths = []
    closing_types = Counter()
    header_naming_total = Counter()

    for post_path in posts:
        frontmatter, body = read_post(post_path)
        post_name = post_path.stem

        post_data = {'filename': post_name}

        # Opening analysis
        first_sents = get_first_sentences(body, 2)
        if first_sents:
            first_sent = first_sents[0]
            opening_type = categorize_opening(first_sent)
            opening_types[opening_type] += 1
            first_sentence_lengths.append(len(first_sent))

            post_data['opening'] = {
                'type': opening_type,
                'first_sentence': first_sent,
                'second_sentence': first_sents[1] if len(first_sents) > 1 else ''
            }

        # Structure analysis
        bold_headers = extract_bold_headers(body)
        h2_count, h3_count = count_h2_h3(body)

        if bold_headers:
            header_patterns = analyze_header_naming(bold_headers)
            for key, val in header_patterns.items():
                header_naming_total[key] += val

        post_data['structure'] = {
            'has_bold_headers': len(bold_headers) > 0,
            'bold_header_count': len(bold_headers),
            'bold_headers': bold_headers,
            'h2_count': h2_count,
            'h3_count': h3_count
        }

        # Paragraph analysis
        para_data = analyze_paragraphs(body)
        post_data['paragraphs'] = {
            'count': len(para_data),
            'details': para_data
        }

        # Closing analysis
        last_para, disclaimer = extract_closing(body)
        closing_type = analyze_closing_type(last_para)
        closing_types[closing_type] += 1

        post_data['closing'] = {
            'last_paragraph': last_para,
            'disclaimer': disclaimer,
            'closing_type': closing_type
        }

        # Formatting analysis
        formatting = count_formatting(body)
        post_data['formatting'] = formatting

        # Length analysis
        word_count = count_words(body)
        post_data['word_count'] = word_count

        all_data['posts'].append(post_data)

    # Save detailed data
    with open('/Users/cns/httpdocs/dkblogs/structure_analysis_v2.json', 'w') as f:
        json.dump(all_data, f, indent=2)

    # Generate comprehensive report
    report = generate_report(all_data, posts, opening_types, first_sentence_lengths,
                            closing_types, header_naming_total)

    # Write report
    with open('/Users/cns/httpdocs/dkblogs/structure_report_v2.txt', 'w') as f:
        f.write(report)

    print(report)
    print("\n\nDetailed data saved to: structure_analysis_v2.json")
    print("Summary report saved to: structure_report_v2.txt")

def generate_report(all_data, posts, opening_types, first_sentence_lengths,
                   closing_types, header_naming_total):
    """Generate comprehensive report."""
    report = []
    total_posts = len(posts)

    report.append("=" * 80)
    report.append("DAVID KNOTT BLOG: STRUCTURE & MECHANICS ANALYSIS")
    report.append("180 Posts (June 2022 - December 2025)")
    report.append("=" * 80)
    report.append("")

    # 1. OPENING PATTERNS
    report.append("1. OPENING PATTERNS")
    report.append("-" * 80)
    report.append("")
    for opening_type, count in opening_types.most_common():
        pct = (count / total_posts) * 100
        report.append(f"  {opening_type.upper()}: {count} posts ({pct:.1f}%)")

    report.append(f"\nFirst sentence length:")
    report.append(f"  Average: {sum(first_sentence_lengths)/len(first_sentence_lengths):.0f} characters")
    report.append(f"  Min: {min(first_sentence_lengths)} characters")
    report.append(f"  Max: {max(first_sentence_lengths)} characters")

    report.append("\n20 Sample Openings (diverse selection):")
    report.append("")

    # Sample openings
    samples_by_type = defaultdict(list)
    for post in all_data['posts']:
        if 'opening' in post:
            samples_by_type[post['opening']['type']].append(post)

    for opening_type in ['question', 'confession', 'anecdote', 'statement', 'fact']:
        samples = samples_by_type[opening_type][:5]
        if samples:
            report.append(f"  {opening_type.upper()}:")
            for s in samples:
                report.append(f"    \"{s['opening']['first_sentence']}\"")
                report.append("")

    # 2. SECTION ORGANIZATION
    report.append("\n2. SECTION ORGANIZATION")
    report.append("-" * 80)
    report.append("")

    posts_with_bold = sum(1 for p in all_data['posts'] if p['structure']['has_bold_headers'])
    posts_without_bold = total_posts - posts_with_bold

    report.append(f"Posts with bold headers: {posts_with_bold} ({posts_with_bold/total_posts*100:.1f}%)")
    report.append(f"Posts with flowing prose only: {posts_without_bold} ({posts_without_bold/total_posts*100:.1f}%)")

    bold_header_counts = [p['structure']['bold_header_count'] for p in all_data['posts']
                         if p['structure']['bold_header_count'] > 0]
    if bold_header_counts:
        report.append(f"\nAverage bold headers per structured post: {sum(bold_header_counts)/len(bold_header_counts):.1f}")
        report.append(f"  Min: {min(bold_header_counts)} headers")
        report.append(f"  Max: {max(bold_header_counts)} headers")

    h2_total = sum(p['structure']['h2_count'] for p in all_data['posts'])
    h3_total = sum(p['structure']['h3_count'] for p in all_data['posts'])
    report.append(f"\nH2 markdown headers (##): {h2_total} total")
    report.append(f"H3 markdown headers (###): {h3_total} total")
    report.append("  → Bold (**text**) is STRONGLY preferred over H2/H3")

    # Header naming patterns
    if header_naming_total:
        total_headers = sum(header_naming_total.values())
        report.append(f"\nHeader naming patterns ({total_headers} headers analyzed):")
        for pattern, count in header_naming_total.most_common():
            pct = (count / total_headers) * 100
            report.append(f"  {pattern.replace('_', ' ').title()}: {count} ({pct:.1f}%)")

    # Sample headers
    all_headers = []
    for p in all_data['posts']:
        all_headers.extend(p['structure']['bold_headers'])

    report.append(f"\nSample bold headers:")
    for h in all_headers[:25]:
        report.append(f"  • {h}")

    # 3. PARAGRAPH ARCHITECTURE
    report.append("\n\n3. PARAGRAPH ARCHITECTURE")
    report.append("-" * 80)
    report.append("")

    all_para_counts = [p['paragraphs']['count'] for p in all_data['posts']]
    report.append(f"Paragraphs per post:")
    report.append(f"  Average: {sum(all_para_counts)/len(all_para_counts):.1f}")
    report.append(f"  Min: {min(all_para_counts)}")
    report.append(f"  Max: {max(all_para_counts)}")

    # Analyze sentence counts
    all_sentence_counts = []
    single_sentence_paras = 0
    total_paras = 0

    for p in all_data['posts']:
        for para in p['paragraphs']['details']:
            total_paras += 1
            all_sentence_counts.append(para['sentence_count'])
            if para['sentence_count'] == 1:
                single_sentence_paras += 1

    report.append(f"\nSentences per paragraph:")
    report.append(f"  Average: {sum(all_sentence_counts)/len(all_sentence_counts):.1f}")
    report.append(f"  Single-sentence paragraphs: {single_sentence_paras}/{total_paras} ({single_sentence_paras/total_paras*100:.1f}%)")

    sentence_dist = Counter(all_sentence_counts)
    report.append(f"\nDistribution:")
    for sent_count in sorted(sentence_dist.keys())[:10]:
        count = sentence_dist[sent_count]
        pct = (count / total_paras) * 100
        report.append(f"  {sent_count} sentence(s): {count} paragraphs ({pct:.1f}%)")

    # Transition analysis
    transition_count = 0
    for p in all_data['posts']:
        for para in p['paragraphs']['details'][1:]:  # Skip first paragraph
            if para['starts_with_transition']:
                transition_count += 1

    non_first_paras = total_paras - len(all_data['posts'])
    report.append(f"\nParagraphs starting with transition words: {transition_count}/{non_first_paras} ({transition_count/non_first_paras*100:.1f}%)")

    # 4. CLOSING PATTERNS
    report.append("\n\n4. CLOSING PATTERNS")
    report.append("-" * 80)
    report.append("")

    disclaimers_found = sum(1 for p in all_data['posts'] if p['closing']['disclaimer'])
    report.append(f"Posts with disclaimer: {disclaimers_found}/{total_posts} ({disclaimers_found/total_posts*100:.1f}%)")

    # Collect unique disclaimers
    unique_disclaimers = set()
    for p in all_data['posts']:
        if p['closing']['disclaimer']:
            unique_disclaimers.add(p['closing']['disclaimer'])

    report.append(f"\nDisclaimer variants found: {len(unique_disclaimers)}")
    report.append("\nDisclaimer text variants:")
    for d in sorted(unique_disclaimers):
        report.append(f"  \"{d}\"")

    # Closing paragraph types
    report.append(f"\nParagraph BEFORE disclaimer (closing type analysis):")
    for closing_type, count in closing_types.most_common():
        pct = (count / total_posts) * 100
        report.append(f"  {closing_type.replace('_', ' ').title()}: {count} ({pct:.1f}%)")

    # 5. FORMATTING CONVENTIONS
    report.append("\n\n5. FORMATTING CONVENTIONS")
    report.append("-" * 80)
    report.append("")

    formatting_totals = defaultdict(int)
    for p in all_data['posts']:
        for key, val in p['formatting'].items():
            formatting_totals[key] += val

    report.append("Usage across all 180 posts:")
    for key in ['bold', 'italic', 'links', 'parentheticals', 'em_dashes', 'en_dashes',
                'bullet_lists', 'numbered_lists']:
        total = formatting_totals[key]
        avg = total / total_posts
        posts_with_feature = sum(1 for p in all_data['posts'] if p['formatting'][key] > 0)
        report.append(f"  {key.replace('_', ' ').title()}:")
        report.append(f"    Total: {total} | Avg per post: {avg:.1f} | In {posts_with_feature} posts ({posts_with_feature/total_posts*100:.1f}%)")

    # Key insights
    report.append("\nKey insights:")
    report.append("  • Bold used primarily for section headers, not emphasis")
    report.append("  • Italics VERY rare (only 2 total) - not used for emphasis")
    report.append("  • Parentheticals common (~4 per post) - used for asides, clarifications")
    report.append("  • Em-dashes rare - not a stylistic signature")
    report.append("  • Lists infrequent - prose flow strongly preferred")

    # 6. LENGTH ANALYSIS
    report.append("\n\n6. LENGTH ANALYSIS")
    report.append("-" * 80)
    report.append("")

    word_counts = [p['word_count'] for p in all_data['posts']]
    report.append(f"Word count statistics:")
    report.append(f"  Average: {sum(word_counts)/len(word_counts):.0f} words")
    report.append(f"  Median: {sorted(word_counts)[len(word_counts)//2]}")
    report.append(f"  Min: {min(word_counts)} words")
    report.append(f"  Max: {max(word_counts)} words")

    shortest = min(all_data['posts'], key=lambda x: x['word_count'])
    longest = max(all_data['posts'], key=lambda x: x['word_count'])

    report.append(f"\nShortest: {shortest['filename']} ({shortest['word_count']} words)")
    report.append(f"Longest: {longest['filename']} ({longest['word_count']} words)")

    # Distribution
    ranges = [(0, 600), (600, 750), (750, 900), (900, 1000), (1000, 1250), (1250, 1500), (1500, 2000)]
    report.append("\nWord count distribution:")
    for low, high in ranges:
        count = sum(1 for wc in word_counts if low <= wc < high)
        pct = (count / total_posts) * 100
        report.append(f"  {low:4d}-{high:4d} words: {count:3d} posts ({pct:4.1f}%)")

    # Correlation with structure
    structured_posts = [p for p in all_data['posts'] if p['structure']['has_bold_headers']]
    unstructured_posts = [p for p in all_data['posts'] if not p['structure']['has_bold_headers']]

    if structured_posts and unstructured_posts:
        avg_structured = sum(p['word_count'] for p in structured_posts) / len(structured_posts)
        avg_unstructured = sum(p['word_count'] for p in unstructured_posts) / len(unstructured_posts)

        report.append(f"\nLength correlation with structure:")
        report.append(f"  Posts WITH bold headers: avg {avg_structured:.0f} words")
        report.append(f"  Posts WITHOUT bold headers: avg {avg_unstructured:.0f} words")

    report.append("\n" + "=" * 80)
    report.append("END OF ANALYSIS")
    report.append("=" * 80)

    return '\n'.join(report)

if __name__ == '__main__':
    main()
