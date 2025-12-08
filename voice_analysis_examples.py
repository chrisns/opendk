#!/usr/bin/env python3
"""
Extract Specific Examples of Voice Patterns
Focus on wit, irony, self-deprecation, and characteristic phrases
"""

import re
from pathlib import Path
from collections import defaultdict

class ExampleExtractor:
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

    def extract_sentences(self, text):
        """Extract sentences from text"""
        # Remove markdown headers
        text = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)
        # Remove code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # Split into sentences
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip() and len(s) > 20]

    def find_self_deprecation(self):
        """Find self-deprecating phrases"""
        patterns = [
            (r"I (don't|do not) (really )?know", "admitting ignorance"),
            (r"I (have no|don't have any) idea", "complete uncertainty"),
            (r"I (was|am) (confused|puzzled|bewildered)", "confusion"),
            (r"my ignorance", "owning ignorance"),
            (r"I (should|must) admit", "reluctant admission"),
            (r"I (was|am) wrong", "admitting error"),
            (r"I (made|make) a mistake", "owning mistakes"),
            (r"I (still )?struggle", "ongoing difficulty"),
            (r"beyond my understanding", "intellectual limits"),
        ]

        examples = defaultdict(list)

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                for pattern, label in patterns:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        examples[label].append({
                            'file': post['filename'],
                            'sentence': sentence
                        })
                        break

        return dict(examples)

    def find_wit_and_irony(self):
        """Find witty or ironic statements"""
        patterns = [
            (r"(of course|naturally)[,.].*?(not|never|isn't|aren't)", "ironic reversal"),
            (r"just.*just", "multiple 'just' irony"),
            (r"simple.*complex|complex.*simple", "complexity irony"),
            (r"easy.*hard|hard.*easy", "difficulty irony"),
            (r"(unfortunately|sadly|alas)", "wry observation"),
            (r"paradox", "paradox"),
            (r"irony|ironic", "explicit irony"),
        ]

        examples = defaultdict(list)

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                for pattern, label in patterns:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        examples[label].append({
                            'file': post['filename'],
                            'sentence': sentence
                        })

        return dict(examples)

    def find_characteristic_phrases(self):
        """Find David's characteristic phrases"""
        phrases = {
            "I think that": [],
            "I believe that": [],
            "perhaps we": [],
            "it seems to me": [],
            "in my experience": [],
            "I have learnt": [],
            "I have seen": [],
            "it turns out": [],
            "the trouble is": [],
            "the challenge is": [],
            "what if we": [],
            "if we're not careful": [],
        }

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                for phrase in phrases.keys():
                    if re.search(re.escape(phrase), sentence, re.IGNORECASE):
                        phrases[phrase].append({
                            'file': post['filename'],
                            'sentence': sentence
                        })

        return phrases

    def find_metaphors_and_analogies(self):
        """Find metaphors and analogies"""
        patterns = [
            r"like a",
            r"as a",
            r"imagine",
            r"think of .* as",
            r"similar to",
            r"reminds me of",
            r"is to .* as .* is to",
        ]

        examples = []

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                for pattern in patterns:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        examples.append({
                            'file': post['filename'],
                            'sentence': sentence
                        })
                        break

        return examples

    def find_rhetorical_questions(self):
        """Find rhetorical questions"""
        examples = []

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                if '?' in sentence:
                    # Look for rhetorical markers
                    if any(marker in sentence.lower() for marker in [
                        'what if', 'why not', 'how can', 'how do we',
                        'isn\'t it', 'aren\'t we', 'don\'t we',
                        'should we', 'could we'
                    ]):
                        examples.append({
                            'file': post['filename'],
                            'sentence': sentence
                        })

        return examples

    def find_qualification_phrases(self):
        """Find phrases that qualify opinions"""
        patterns = {
            "in my view": [],
            "in my opinion": [],
            "I would argue": [],
            "I would suggest": [],
            "I suspect": [],
            "it seems likely": [],
            "arguably": [],
            "tend to": [],
            "generally": [],
            "often": [],
        }

        for post in self.posts:
            sentences = self.extract_sentences(post['content'])
            for sentence in sentences:
                for phrase in patterns.keys():
                    if re.search(re.escape(phrase), sentence, re.IGNORECASE):
                        patterns[phrase].append({
                            'file': post['filename'],
                            'sentence': sentence[:300]
                        })

        return patterns

    def generate_report(self):
        """Generate examples report"""
        print("Loading posts...")
        self.load_posts()

        report = []
        report.append("=" * 80)
        report.append("VOICE PATTERN EXAMPLES: WIT, IRONY & CHARACTERISTIC PHRASES")
        report.append("=" * 80)

        # Self-deprecation
        print("Finding self-deprecation...")
        self_dep = self.find_self_deprecation()

        report.append("\n## SELF-DEPRECATION & HUMILITY")
        for category, examples in sorted(self_dep.items(), key=lambda x: len(x[1]), reverse=True):
            report.append(f"\n### {category.upper()} ({len(examples)} examples)")
            for ex in examples[:5]:
                report.append(f"  \"{ex['sentence']}\"")
                report.append(f"  [{ex['file']}]\n")

        # Wit and irony
        print("Finding wit and irony...")
        wit = self.find_wit_and_irony()

        report.append("\n" + "=" * 80)
        report.append("## WIT & IRONY")
        for category, examples in sorted(wit.items(), key=lambda x: len(x[1]), reverse=True):
            if examples:
                report.append(f"\n### {category.upper()} ({len(examples)} examples)")
                for ex in examples[:5]:
                    report.append(f"  \"{ex['sentence']}\"")
                    report.append(f"  [{ex['file']}]\n")

        # Characteristic phrases
        print("Finding characteristic phrases...")
        phrases = self.find_characteristic_phrases()

        report.append("\n" + "=" * 80)
        report.append("## CHARACTERISTIC PHRASES")
        for phrase, examples in sorted(phrases.items(), key=lambda x: len(x[1]), reverse=True):
            if examples:
                report.append(f"\n### \"{phrase.upper()}\" ({len(examples)} uses)")
                for ex in examples[:3]:
                    report.append(f"  \"{ex['sentence']}\"")
                    report.append(f"  [{ex['file']}]\n")

        # Qualification phrases
        print("Finding qualification phrases...")
        qual = self.find_qualification_phrases()

        report.append("\n" + "=" * 80)
        report.append("## QUALIFICATION & HEDGING PHRASES")
        for phrase, examples in sorted(qual.items(), key=lambda x: len(x[1]), reverse=True):
            if examples:
                report.append(f"\n### \"{phrase.upper()}\" ({len(examples)} uses)")
                for ex in examples[:3]:
                    report.append(f"  \"{ex['sentence']}...\"")
                    report.append(f"  [{ex['file']}]\n")

        # Metaphors
        print("Finding metaphors and analogies...")
        metaphors = self.find_metaphors_and_analogies()

        report.append("\n" + "=" * 80)
        report.append(f"## METAPHORS & ANALOGIES ({len(metaphors)} examples)")
        for ex in metaphors[:20]:
            report.append(f"  \"{ex['sentence']}\"")
            report.append(f"  [{ex['file']}]\n")

        # Rhetorical questions
        print("Finding rhetorical questions...")
        rhetorical = self.find_rhetorical_questions()

        report.append("\n" + "=" * 80)
        report.append(f"## RHETORICAL QUESTIONS ({len(rhetorical)} examples)")
        for ex in rhetorical[:20]:
            report.append(f"  \"{ex['sentence']}\"")
            report.append(f"  [{ex['file']}]\n")

        return "\n".join(report)

if __name__ == "__main__":
    extractor = ExampleExtractor("/Users/cns/httpdocs/dkblogs")
    report = extractor.generate_report()

    output_file = "/Users/cns/httpdocs/dkblogs/voice_analysis_examples_report.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nExample extraction complete! Report saved to: {output_file}")
    print("\n" + "="*80)
    print(report)
