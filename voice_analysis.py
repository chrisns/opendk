#!/usr/bin/env python3
"""
Comprehensive Voice & Pronoun Pattern Analysis for David Knott's Blog
Analyzes 180+ blog posts for voice, pronoun usage, hedging, and reader relationship patterns
"""

import re
import os
from collections import defaultdict, Counter
from pathlib import Path
import json

class VoiceAnalyzer:
    def __init__(self, blog_dir):
        self.blog_dir = Path(blog_dir)
        self.posts = []
        self.stats = {
            'first_person_i': defaultdict(list),
            'first_person_plural': defaultdict(list),
            'second_person': defaultdict(list),
            'hedging': defaultdict(list),
            'assertions': defaultdict(list),
            'emotional': defaultdict(list),
            'total_sentences': 0,
            'total_words': 0,
        }

    def load_posts(self):
        """Load all markdown blog posts"""
        md_files = sorted(self.blog_dir.glob('*.md'))
        # Exclude backup directories
        md_files = [f for f in md_files if '_backup' not in str(f)]

        for filepath in md_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.posts.append({
                        'filename': filepath.name,
                        'content': content,
                        'date': filepath.name[:10]  # Extract YYYY-MM-DD
                    })
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

        print(f"Loaded {len(self.posts)} blog posts")
        return len(self.posts)

    def extract_sentences(self, text):
        """Extract sentences from text, handling markdown"""
        # Remove markdown headers
        text = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)
        # Remove code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # Remove inline code
        text = re.sub(r'`[^`]+`', '', text)
        # Split into sentences (basic - handles . ! ?)
        sentences = re.split(r'[.!?]+\s+', text)
        # Clean up
        sentences = [s.strip() for s in sentences if s.strip() and len(s) > 10]
        return sentences

    def analyze_first_person_i(self):
        """Analyze 'I' usage patterns"""
        patterns = {
            'i_think': r'\bI think\b',
            'i_believe': r'\bI believe\b',
            'i_must_admit': r'\bI must admit\b',
            'i_confess': r'\bI confess\b',
            'i_suspect': r'\bI suspect\b',
            'i_have': r'\bI have\b',
            'i_ve': r"\bI've\b",
            'i_remember': r'\bI remember\b',
            'i_find': r'\bI find\b',
            'i_would': r'\bI would\b',
            'i_can': r'\bI can\b',
            'i_dont': r"\bI don't\b",
            'i_like': r'\bI like\b',
            'i_love': r'\bI love\b',
            'i_want': r'\bI want\b',
            'i_need': r'\bI need\b',
            'i_feel': r'\bI feel\b',
            'i_wonder': r'\bI wonder\b',
            'i_worry': r'\bI worry\b',
        }

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                for pattern_name, pattern in patterns.items():
                    matches = re.finditer(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        self.stats['first_person_i'][pattern_name].append({
                            'file': post['filename'],
                            'sentence': sentence[:200]  # First 200 chars
                        })

    def analyze_first_person_plural(self):
        """Analyze 'we' usage patterns"""
        patterns = {
            'we_should': r'\bwe should\b',
            'we_must': r'\bwe must\b',
            'we_need': r'\bwe need\b',
            'we_can': r'\bwe can\b',
            'we_have': r'\bwe have\b',
            'we_are': r'\bwe are\b',
            'we_re': r"\bwe're\b",
            'we_could': r'\bwe could\b',
            'we_might': r'\bwe might\b',
            'we_want': r'\bwe want\b',
        }

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                for pattern_name, pattern in patterns.items():
                    matches = re.finditer(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        self.stats['first_person_plural'][pattern_name].append({
                            'file': post['filename'],
                            'sentence': sentence[:200]
                        })

    def analyze_second_person(self):
        """Analyze 'you' patterns"""
        patterns = {
            'if_you': r'\bif you\b',
            'you_might': r'\byou might\b',
            'you_may': r'\byou may\b',
            'you_should': r'\byou should\b',
            'you_can': r'\byou can\b',
            'you_need': r'\byou need\b',
            'you_have': r'\byou have\b',
            'you_are': r'\byou are\b',
            'you_re': r"\byou're\b",
            'you_could': r'\byou could\b',
            'you_want': r'\byou want\b',
            'you_will': r'\byou will\b',
        }

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                for pattern_name, pattern in patterns.items():
                    matches = re.finditer(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        self.stats['second_person'][pattern_name].append({
                            'file': post['filename'],
                            'sentence': sentence[:200]
                        })

    def analyze_hedging(self):
        """Analyze hedging language"""
        patterns = {
            'perhaps': r'\bperhaps\b',
            'maybe': r'\bmaybe\b',
            'probably': r'\bprobably\b',
            'possibly': r'\bpossibly\b',
            'it_seems': r'\bit seems\b',
            'seems_to_me': r'\bseems to me\b',
            'seems_likely': r'\bseems likely\b',
            'might': r'\bmight\b',
            'may': r'\bmay\b',
            'could': r'\bcould\b',
            'arguably': r'\barguably\b',
            'tend_to': r'\btend to\b',
            'in_my_view': r'\bin my view\b',
            'in_my_opinion': r'\bin my opinion\b',
            'i_suspect': r'\bI suspect\b',
        }

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                for pattern_name, pattern in patterns.items():
                    matches = re.finditer(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        self.stats['hedging'][pattern_name].append({
                            'file': post['filename'],
                            'sentence': sentence[:200]
                        })

    def analyze_assertions(self):
        """Analyze strong assertion patterns"""
        patterns = {
            'we_must': r'\bwe must\b',
            'it_is_essential': r'\bit is essential\b',
            'it_is_important': r'\bit is important\b',
            'it_is_critical': r'\bit is critical\b',
            'it_is_crucial': r'\bit is crucial\b',
            'you_must': r'\byou must\b',
            'you_should': r'\byou should\b',
            'this_is_important': r'\bthis is important\b',
            'clearly': r'\bclearly\b',
            'obviously': r'\bobviously\b',
            'undoubtedly': r'\bundoubtedly\b',
            'certainly': r'\bcertainly\b',
            'definitely': r'\bdefinitely\b',
        }

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                for pattern_name, pattern in patterns.items():
                    matches = re.finditer(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        self.stats['assertions'][pattern_name].append({
                            'file': post['filename'],
                            'sentence': sentence[:200]
                        })

    def analyze_emotional_register(self):
        """Analyze emotional register and self-deprecation"""
        patterns = {
            # Self-deprecation
            'i_dont_know': r"\bI don't know\b",
            'i_have_no_idea': r"\bI have no idea\b",
            'im_not_sure': r"\bI'm not sure\b",
            'im_confused': r"\bI'm confused\b",
            'my_ignorance': r'\bmy ignorance\b',

            # Humor markers
            'of_course': r'\bof course\b',
            'ironically': r'\bironica(lly)?\b',
            'amusingly': r'\bamusi(ng|ngly)\b',

            # Passion/frustration
            'frustrated': r'\bfrustra(ted|ting)\b',
            'excited': r'\bexcited\b',
            'worried': r'\bworried\b',
            'concerned': r'\bconcerned\b',
            'fascinated': r'\bfascinat(ed|ing)\b',

            # Humility
            'i_was_wrong': r'\bI was wrong\b',
            'i_made_a_mistake': r'\bI made a mistake\b',
            'i_learnt': r'\bI learnt\b',
            'i_learned': r'\bI learned\b',
        }

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                for pattern_name, pattern in patterns.items():
                    matches = re.finditer(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        self.stats['emotional'][pattern_name].append({
                            'file': post['filename'],
                            'sentence': sentence[:200]
                        })

    def count_total_stats(self):
        """Count total words and sentences"""
        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            self.stats['total_sentences'] += len(sentences)
            words = re.findall(r'\b\w+\b', post['content'])
            self.stats['total_words'] += len(words)

    def generate_report(self):
        """Generate comprehensive analysis report"""
        report = []
        report.append("=" * 80)
        report.append("DAVID KNOTT BLOG VOICE & PRONOUN PATTERN ANALYSIS")
        report.append("=" * 80)
        report.append(f"\nTotal posts analyzed: {len(self.posts)}")
        report.append(f"Total sentences: {self.stats['total_sentences']:,}")
        report.append(f"Total words: {self.stats['total_words']:,}")
        report.append(f"Date range: {self.posts[0]['date']} to {self.posts[-1]['date']}")

        # 1. FIRST PERSON "I" PATTERNS
        report.append("\n" + "=" * 80)
        report.append("1. FIRST PERSON 'I' USAGE PATTERNS")
        report.append("=" * 80)

        i_total = sum(len(v) for v in self.stats['first_person_i'].values())
        report.append(f"\nTotal 'I' pattern occurrences: {i_total}")
        report.append(f"Average per post: {i_total / len(self.posts):.1f}")

        # Sort by frequency
        i_patterns = [(k, len(v)) for k, v in self.stats['first_person_i'].items()]
        i_patterns.sort(key=lambda x: x[1], reverse=True)

        report.append("\nFrequency breakdown:")
        for pattern, count in i_patterns:
            pct = (count / self.stats['total_sentences'] * 100) if self.stats['total_sentences'] > 0 else 0
            report.append(f"  {pattern:20s}: {count:4d} occurrences ({pct:.2f}% of sentences)")

        # Examples for top patterns
        report.append("\nEXAMPLES OF TOP 'I' PATTERNS:")
        for pattern, count in i_patterns[:5]:
            examples = self.stats['first_person_i'][pattern][:3]
            report.append(f"\n  {pattern.upper()} ({count} occurrences):")
            for ex in examples:
                report.append(f"    - \"{ex['sentence']}...\"")
                report.append(f"      [{ex['file']}]")

        # 2. FIRST PERSON PLURAL "WE"
        report.append("\n" + "=" * 80)
        report.append("2. FIRST PERSON PLURAL 'WE' PATTERNS")
        report.append("=" * 80)

        we_total = sum(len(v) for v in self.stats['first_person_plural'].values())
        report.append(f"\nTotal 'we' pattern occurrences: {we_total}")
        report.append(f"Average per post: {we_total / len(self.posts):.1f}")

        we_patterns = [(k, len(v)) for k, v in self.stats['first_person_plural'].items()]
        we_patterns.sort(key=lambda x: x[1], reverse=True)

        report.append("\nFrequency breakdown:")
        for pattern, count in we_patterns:
            pct = (count / self.stats['total_sentences'] * 100) if self.stats['total_sentences'] > 0 else 0
            report.append(f"  {pattern:20s}: {count:4d} occurrences ({pct:.2f}% of sentences)")

        report.append("\nEXAMPLES OF TOP 'WE' PATTERNS:")
        for pattern, count in we_patterns[:5]:
            examples = self.stats['first_person_plural'][pattern][:3]
            report.append(f"\n  {pattern.upper()} ({count} occurrences):")
            for ex in examples:
                report.append(f"    - \"{ex['sentence']}...\"")
                report.append(f"      [{ex['file']}]")

        # 3. SECOND PERSON "YOU"
        report.append("\n" + "=" * 80)
        report.append("3. SECOND PERSON 'YOU' PATTERNS")
        report.append("=" * 80)

        you_total = sum(len(v) for v in self.stats['second_person'].values())
        report.append(f"\nTotal 'you' pattern occurrences: {you_total}")
        report.append(f"Average per post: {you_total / len(self.posts):.1f}")

        you_patterns = [(k, len(v)) for k, v in self.stats['second_person'].items()]
        you_patterns.sort(key=lambda x: x[1], reverse=True)

        report.append("\nFrequency breakdown:")
        for pattern, count in you_patterns:
            pct = (count / self.stats['total_sentences'] * 100) if self.stats['total_sentences'] > 0 else 0
            report.append(f"  {pattern:20s}: {count:4d} occurrences ({pct:.2f}% of sentences)")

        report.append("\nEXAMPLES OF TOP 'YOU' PATTERNS:")
        for pattern, count in you_patterns[:5]:
            examples = self.stats['second_person'][pattern][:3]
            report.append(f"\n  {pattern.upper()} ({count} occurrences):")
            for ex in examples:
                report.append(f"    - \"{ex['sentence']}...\"")
                report.append(f"      [{ex['file']}]")

        # 4. HEDGING LANGUAGE
        report.append("\n" + "=" * 80)
        report.append("4. HEDGING LANGUAGE")
        report.append("=" * 80)

        hedge_total = sum(len(v) for v in self.stats['hedging'].values())
        report.append(f"\nTotal hedging occurrences: {hedge_total}")
        report.append(f"Average per post: {hedge_total / len(self.posts):.1f}")

        hedge_patterns = [(k, len(v)) for k, v in self.stats['hedging'].items()]
        hedge_patterns.sort(key=lambda x: x[1], reverse=True)

        report.append("\nFrequency breakdown:")
        for pattern, count in hedge_patterns:
            pct = (count / self.stats['total_sentences'] * 100) if self.stats['total_sentences'] > 0 else 0
            report.append(f"  {pattern:20s}: {count:4d} occurrences ({pct:.2f}% of sentences)")

        report.append("\nEXAMPLES OF TOP HEDGING PATTERNS:")
        for pattern, count in hedge_patterns[:5]:
            examples = self.stats['hedging'][pattern][:3]
            report.append(f"\n  {pattern.upper()} ({count} occurrences):")
            for ex in examples:
                report.append(f"    - \"{ex['sentence']}...\"")
                report.append(f"      [{ex['file']}]")

        # 5. ASSERTION PATTERNS
        report.append("\n" + "=" * 80)
        report.append("5. ASSERTION PATTERNS")
        report.append("=" * 80)

        assert_total = sum(len(v) for v in self.stats['assertions'].values())
        report.append(f"\nTotal assertion occurrences: {assert_total}")
        report.append(f"Average per post: {assert_total / len(self.posts):.1f}")

        assert_patterns = [(k, len(v)) for k, v in self.stats['assertions'].items()]
        assert_patterns.sort(key=lambda x: x[1], reverse=True)

        report.append("\nFrequency breakdown:")
        for pattern, count in assert_patterns:
            pct = (count / self.stats['total_sentences'] * 100) if self.stats['total_sentences'] > 0 else 0
            report.append(f"  {pattern:20s}: {count:4d} occurrences ({pct:.2f}% of sentences)")

        report.append("\nEXAMPLES OF TOP ASSERTION PATTERNS:")
        for pattern, count in assert_patterns[:5]:
            examples = self.stats['assertions'][pattern][:3]
            report.append(f"\n  {pattern.upper()} ({count} occurrences):")
            for ex in examples:
                report.append(f"    - \"{ex['sentence']}...\"")
                report.append(f"      [{ex['file']}]")

        # 6. EMOTIONAL REGISTER
        report.append("\n" + "=" * 80)
        report.append("6. EMOTIONAL REGISTER & SELF-DEPRECATION")
        report.append("=" * 80)

        emotion_total = sum(len(v) for v in self.stats['emotional'].values())
        report.append(f"\nTotal emotional/humility markers: {emotion_total}")
        report.append(f"Average per post: {emotion_total / len(self.posts):.1f}")

        emotion_patterns = [(k, len(v)) for k, v in self.stats['emotional'].items()]
        emotion_patterns.sort(key=lambda x: x[1], reverse=True)

        report.append("\nFrequency breakdown:")
        for pattern, count in emotion_patterns:
            pct = (count / self.stats['total_sentences'] * 100) if self.stats['total_sentences'] > 0 else 0
            report.append(f"  {pattern:20s}: {count:4d} occurrences ({pct:.2f}% of sentences)")

        report.append("\nEXAMPLES OF EMOTIONAL REGISTER:")
        for pattern, count in emotion_patterns[:8]:
            examples = self.stats['emotional'][pattern][:2]
            report.append(f"\n  {pattern.upper()} ({count} occurrences):")
            for ex in examples:
                report.append(f"    - \"{ex['sentence']}...\"")
                report.append(f"      [{ex['file']}]")

        # 7. COMPARATIVE ANALYSIS
        report.append("\n" + "=" * 80)
        report.append("7. COMPARATIVE VOICE ANALYSIS")
        report.append("=" * 80)

        report.append(f"\nVoice distribution:")
        report.append(f"  First person 'I':        {i_total:4d} occurrences")
        report.append(f"  First person plural 'we': {we_total:4d} occurrences")
        report.append(f"  Second person 'you':      {you_total:4d} occurrences")
        report.append(f"\nHedging vs Assertion:")
        report.append(f"  Hedging language:         {hedge_total:4d} occurrences")
        report.append(f"  Strong assertions:        {assert_total:4d} occurrences")
        report.append(f"  Hedge/Assert ratio:       {hedge_total/assert_total:.2f}:1")

        return "\n".join(report)

    def run_analysis(self):
        """Run complete analysis"""
        print("Loading blog posts...")
        self.load_posts()

        print("Analyzing first person 'I' patterns...")
        self.analyze_first_person_i()

        print("Analyzing first person plural 'we' patterns...")
        self.analyze_first_person_plural()

        print("Analyzing second person 'you' patterns...")
        self.analyze_second_person()

        print("Analyzing hedging language...")
        self.analyze_hedging()

        print("Analyzing assertion patterns...")
        self.analyze_assertions()

        print("Analyzing emotional register...")
        self.analyze_emotional_register()

        print("Counting total statistics...")
        self.count_total_stats()

        print("Generating report...")
        report = self.generate_report()

        return report

if __name__ == "__main__":
    analyzer = VoiceAnalyzer("/Users/cns/httpdocs/dkblogs")
    report = analyzer.run_analysis()

    # Save report to file
    output_file = "/Users/cns/httpdocs/dkblogs/voice_analysis_report.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nAnalysis complete! Report saved to: {output_file}")
    print("\n" + "="*80)
    print(report)
