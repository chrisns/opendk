#!/usr/bin/env python3
"""
Deep Voice Analysis - Context, Transitions, and Stylistic Patterns
Analyzes when David shifts voice, opening/closing patterns, and topic-specific hedging
"""

import re
from pathlib import Path
from collections import defaultdict

class DeepVoiceAnalyzer:
    def __init__(self, blog_dir):
        self.blog_dir = Path(blog_dir)
        self.posts = []

    def load_posts(self):
        """Load all markdown blog posts"""
        md_files = sorted(self.blog_dir.glob('*.md'))
        md_files = [f for f in md_files if '_backup' not in str(f)]

        for filepath in md_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.posts.append({
                        'filename': filepath.name,
                        'content': content,
                        'date': filepath.name[:10]
                    })
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

        return len(self.posts)

    def extract_paragraphs(self, text):
        """Extract paragraphs, removing markdown"""
        # Remove frontmatter
        text = re.sub(r'^---.*?---', '', text, flags=re.DOTALL)
        # Remove headers
        text = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)
        # Remove code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # Split by double newline
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip() and len(p) > 30]

    def analyze_voice_transitions(self):
        """Analyze when David shifts from I to we, we to you, etc."""
        transitions = []

        for post in self.posts:
            paragraphs = self.extract_paragraphs(post['content'])

            for i, para in enumerate(paragraphs):
                has_i = bool(re.search(r'\bI\b', para))
                has_we = bool(re.search(r'\bwe\b', para, re.IGNORECASE))
                has_you = bool(re.search(r'\byou\b', para, re.IGNORECASE))

                if i > 0:
                    prev_para = paragraphs[i-1]
                    prev_i = bool(re.search(r'\bI\b', prev_para))
                    prev_we = bool(re.search(r'\bwe\b', prev_para, re.IGNORECASE))
                    prev_you = bool(re.search(r'\byou\b', prev_para, re.IGNORECASE))

                    # Detect transitions
                    if prev_i and has_we and not prev_we:
                        transitions.append({
                            'type': 'I to we',
                            'file': post['filename'],
                            'from': prev_para[:150],
                            'to': para[:150]
                        })
                    elif prev_we and has_you and not prev_you:
                        transitions.append({
                            'type': 'we to you',
                            'file': post['filename'],
                            'from': prev_para[:150],
                            'to': para[:150]
                        })
                    elif prev_i and has_you and not prev_i:
                        transitions.append({
                            'type': 'I to you',
                            'file': post['filename'],
                            'from': prev_para[:150],
                            'to': para[:150]
                        })

        return transitions

    def analyze_opening_patterns(self):
        """Analyze how posts open - hedged vs assertive, voice choice"""
        openings = []

        for post in self.posts:
            paragraphs = self.extract_paragraphs(post['content'])
            if not paragraphs:
                continue

            first_para = paragraphs[0]
            first_sentence = re.split(r'[.!?]\s+', first_para)[0]

            has_i = bool(re.search(r'\bI\b', first_sentence))
            has_we = bool(re.search(r'\bwe\b', first_sentence, re.IGNORECASE))
            has_you = bool(re.search(r'\byou\b', first_sentence, re.IGNORECASE))

            # Check for hedging
            hedges = ['perhaps', 'maybe', 'might', 'may', 'could', 'possibly']
            has_hedge = any(re.search(fr'\b{h}\b', first_sentence, re.IGNORECASE) for h in hedges)

            # Check for assertions
            assertions = ['must', 'should', 'essential', 'important', 'critical']
            has_assertion = any(re.search(fr'\b{a}\b', first_sentence, re.IGNORECASE) for a in assertions)

            # Check for questions
            is_question = '?' in first_sentence

            openings.append({
                'file': post['filename'],
                'sentence': first_sentence,
                'has_i': has_i,
                'has_we': has_we,
                'has_you': has_you,
                'has_hedge': has_hedge,
                'has_assertion': has_assertion,
                'is_question': is_question
            })

        return openings

    def analyze_closing_patterns(self):
        """Analyze how posts close - more/less assertive?"""
        closings = []

        for post in self.posts:
            paragraphs = self.extract_paragraphs(post['content'])
            if len(paragraphs) < 2:
                continue

            last_para = paragraphs[-1]
            sentences = re.split(r'[.!?]\s+', last_para)
            last_sentence = sentences[-1] if sentences else ""

            has_i = bool(re.search(r'\bI\b', last_sentence))
            has_we = bool(re.search(r'\bwe\b', last_sentence, re.IGNORECASE))
            has_you = bool(re.search(r'\byou\b', last_sentence, re.IGNORECASE))

            # Check for hedging
            hedges = ['perhaps', 'maybe', 'might', 'may', 'could', 'possibly']
            has_hedge = any(re.search(fr'\b{h}\b', last_sentence, re.IGNORECASE) for h in hedges)

            # Check for assertions
            assertions = ['must', 'should', 'essential', 'important', 'critical']
            has_assertion = any(re.search(fr'\b{a}\b', last_sentence, re.IGNORECASE) for a in assertions)

            # Check for call to action
            has_cta = bool(re.search(r'\b(let\'s|try|consider|think about|ask yourself)\b', last_sentence, re.IGNORECASE))

            closings.append({
                'file': post['filename'],
                'sentence': last_sentence,
                'has_i': has_i,
                'has_we': has_we,
                'has_you': has_you,
                'has_hedge': has_hedge,
                'has_assertion': has_assertion,
                'has_cta': has_cta
            })

        return closings

    def analyze_reader_positioning(self):
        """Analyze how David positions the reader"""
        patterns = {
            'collaborative': [
                r'\blet\'s\b',
                r'\btogether\b',
                r'\bour\b',
                r'\bwe can\b',
            ],
            'questioning': [
                r'^(What|How|Why|When|Where|Do you|Can you|Should you|Have you)',
                r'\?$',
            ],
            'authoritative': [
                r'\byou must\b',
                r'\byou should\b',
                r'\byou need to\b',
                r'\bit is essential\b',
            ],
            'peer': [
                r'\bas technologists\b',
                r'\bas engineers\b',
                r'\bas developers\b',
                r'\bwe all\b',
            ],
            'empathetic': [
                r'\bI understand\b',
                r'\bI know\b',
                r'\bI\'ve been there\b',
                r'\bit\'s hard\b',
                r'\bit\'s difficult\b',
            ]
        }

        results = defaultdict(list)

        for post in self.posts:
            paragraphs = self.extract_paragraphs(post['content'])
            for para in paragraphs:
                for category, pattern_list in patterns.items():
                    for pattern in pattern_list:
                        if re.search(pattern, para, re.IGNORECASE):
                            results[category].append({
                                'file': post['filename'],
                                'excerpt': para[:200]
                            })
                            break  # Only count once per paragraph

        return results

    def analyze_topic_specific_confidence(self):
        """Analyze confidence levels by topic"""
        topics = {
            'cloud': ['cloud', 'aws', 'azure', 'gcp', 'infrastructure'],
            'ai': ['ai', 'machine learning', 'generative', 'llm', 'gpt', 'chatgpt'],
            'quantum': ['quantum', 'qubit', 'superposition'],
            'legacy': ['legacy', 'modernisation', 'modernization', 'technical debt'],
            'architecture': ['architecture', 'design', 'pattern', 'microservice'],
            'people': ['team', 'people', 'culture', 'leadership', 'management']
        }

        topic_confidence = defaultdict(lambda: {'hedged': 0, 'assertive': 0, 'total': 0})

        hedges = ['perhaps', 'maybe', 'might', 'may', 'could', 'possibly', 'probably', 'i think', 'i believe']
        assertions = ['must', 'should', 'essential', 'important', 'critical', 'clearly', 'obviously', 'certainly']

        for post in self.posts:
            content = post['content'].lower()

            for topic_name, keywords in topics.items():
                # Check if post is about this topic
                if any(keyword in content for keyword in keywords):
                    paragraphs = self.extract_paragraphs(post['content'])

                    for para in paragraphs:
                        # Check if paragraph mentions topic
                        if any(keyword in para.lower() for keyword in keywords):
                            topic_confidence[topic_name]['total'] += 1

                            has_hedge = any(re.search(fr'\b{h}\b', para, re.IGNORECASE) for h in hedges)
                            has_assertion = any(re.search(fr'\b{a}\b', para, re.IGNORECASE) for a in assertions)

                            if has_hedge:
                                topic_confidence[topic_name]['hedged'] += 1
                            if has_assertion:
                                topic_confidence[topic_name]['assertive'] += 1

        return dict(topic_confidence)

    def generate_report(self):
        """Generate deep analysis report"""
        print("Loading posts...")
        self.load_posts()

        report = []
        report.append("=" * 80)
        report.append("DEEP VOICE ANALYSIS: CONTEXT, TRANSITIONS & STYLISTIC PATTERNS")
        report.append("=" * 80)

        # Voice transitions
        print("Analyzing voice transitions...")
        transitions = self.analyze_voice_transitions()
        report.append("\n## VOICE TRANSITION PATTERNS")
        report.append(f"Total detected transitions: {len(transitions)}")

        transition_types = defaultdict(int)
        for t in transitions:
            transition_types[t['type']] += 1

        report.append("\nTransition frequency:")
        for ttype, count in transition_types.items():
            report.append(f"  {ttype}: {count} occurrences")

        report.append("\nExample transitions:")
        for ttype in ['I to we', 'we to you', 'I to you']:
            examples = [t for t in transitions if t['type'] == ttype][:2]
            if examples:
                report.append(f"\n  {ttype.upper()}:")
                for ex in examples:
                    report.append(f"    From: \"{ex['from']}...\"")
                    report.append(f"    To:   \"{ex['to']}...\"")
                    report.append(f"    [{ex['file']}]\n")

        # Opening patterns
        print("Analyzing opening patterns...")
        openings = self.analyze_opening_patterns()

        report.append("\n" + "=" * 80)
        report.append("## OPENING SENTENCE PATTERNS")
        report.append("=" * 80)

        i_openings = sum(1 for o in openings if o['has_i'])
        we_openings = sum(1 for o in openings if o['has_we'])
        you_openings = sum(1 for o in openings if o['has_you'])
        question_openings = sum(1 for o in openings if o['is_question'])
        hedged_openings = sum(1 for o in openings if o['has_hedge'])
        assertive_openings = sum(1 for o in openings if o['has_assertion'])

        total = len(openings)
        report.append(f"\nVoice in opening sentences:")
        report.append(f"  Starts with 'I':         {i_openings:3d} ({i_openings/total*100:.1f}%)")
        report.append(f"  Starts with 'we':        {we_openings:3d} ({we_openings/total*100:.1f}%)")
        report.append(f"  Starts with 'you':       {you_openings:3d} ({you_openings/total*100:.1f}%)")
        report.append(f"  Opens with question:     {question_openings:3d} ({question_openings/total*100:.1f}%)")
        report.append(f"  Opens with hedge:        {hedged_openings:3d} ({hedged_openings/total*100:.1f}%)")
        report.append(f"  Opens with assertion:    {assertive_openings:3d} ({assertive_openings/total*100:.1f}%)")

        report.append("\nExample question openings:")
        for opening in [o for o in openings if o['is_question']][:5]:
            report.append(f"  \"{opening['sentence']}\"")
            report.append(f"  [{opening['file']}]\n")

        # Closing patterns
        print("Analyzing closing patterns...")
        closings = self.analyze_closing_patterns()

        report.append("\n" + "=" * 80)
        report.append("## CLOSING SENTENCE PATTERNS")
        report.append("=" * 80)

        i_closings = sum(1 for c in closings if c['has_i'])
        we_closings = sum(1 for c in closings if c['has_we'])
        you_closings = sum(1 for c in closings if c['has_you'])
        hedged_closings = sum(1 for c in closings if c['has_hedge'])
        assertive_closings = sum(1 for c in closings if c['has_assertion'])
        cta_closings = sum(1 for c in closings if c['has_cta'])

        total = len(closings)
        report.append(f"\nVoice in closing sentences:")
        report.append(f"  Closes with 'I':         {i_closings:3d} ({i_closings/total*100:.1f}%)")
        report.append(f"  Closes with 'we':        {we_closings:3d} ({we_closings/total*100:.1f}%)")
        report.append(f"  Closes with 'you':       {you_closings:3d} ({you_closings/total*100:.1f}%)")
        report.append(f"  Closes with hedge:       {hedged_closings:3d} ({hedged_closings/total*100:.1f}%)")
        report.append(f"  Closes with assertion:   {assertive_closings:3d} ({assertive_closings/total*100:.1f}%)")
        report.append(f"  Closes with CTA:         {cta_closings:3d} ({cta_closings/total*100:.1f}%)")

        report.append("\nExample call-to-action closings:")
        for closing in [c for c in closings if c['has_cta']][:5]:
            report.append(f"  \"{closing['sentence']}\"")
            report.append(f"  [{closing['file']}]\n")

        # Reader positioning
        print("Analyzing reader positioning...")
        positioning = self.analyze_reader_positioning()

        report.append("\n" + "=" * 80)
        report.append("## READER RELATIONSHIP & POSITIONING")
        report.append("=" * 80)

        for category, instances in positioning.items():
            report.append(f"\n{category.upper()} stance: {len(instances)} occurrences")
            for instance in instances[:3]:
                report.append(f"  \"{instance['excerpt']}...\"")
                report.append(f"  [{instance['file']}]\n")

        # Topic-specific confidence
        print("Analyzing topic-specific confidence...")
        topic_conf = self.analyze_topic_specific_confidence()

        report.append("\n" + "=" * 80)
        report.append("## TOPIC-SPECIFIC CONFIDENCE CALIBRATION")
        report.append("=" * 80)

        for topic, stats in sorted(topic_conf.items(), key=lambda x: x[1]['total'], reverse=True):
            if stats['total'] > 0:
                hedge_pct = (stats['hedged'] / stats['total'] * 100) if stats['total'] > 0 else 0
                assert_pct = (stats['assertive'] / stats['total'] * 100) if stats['total'] > 0 else 0
                report.append(f"\n{topic.upper()}:")
                report.append(f"  Total paragraphs: {stats['total']}")
                report.append(f"  Hedged:           {stats['hedged']:3d} ({hedge_pct:.1f}%)")
                report.append(f"  Assertive:        {stats['assertive']:3d} ({assert_pct:.1f}%)")
                if stats['hedged'] > 0 and stats['assertive'] > 0:
                    ratio = stats['hedged'] / stats['assertive']
                    report.append(f"  Hedge/Assert:     {ratio:.2f}:1")

        return "\n".join(report)

if __name__ == "__main__":
    analyzer = DeepVoiceAnalyzer("/Users/cns/httpdocs/dkblogs")
    report = analyzer.generate_report()

    output_file = "/Users/cns/httpdocs/dkblogs/voice_analysis_deep_report.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nDeep analysis complete! Report saved to: {output_file}")
    print("\n" + "="*80)
    print(report)
