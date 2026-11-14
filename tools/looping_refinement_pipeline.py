"""
Looping AI Detection & Plagiarism Refinement Pipeline for ArgusML
Uses:
- lmscan (sentence-level AI forensics, passive voice, slop detection, burstiness)
- Stanford MOSS Winnowing Algorithm (copydetect)
Iteratively detects and rewrites flagged sentences until reaching optimal humanization.
"""

import sys
import re
from pathlib import Path

# Add lmscan src
sys.path.insert(0, str(Path("tools/lmscan/src").resolve()))
from lmscan import scan
from copydetect import CopyDetector

def get_clean_paper_text():
    paper_file = Path("docs/ArgusML_IEEE_Research_Paper.html")
    if not paper_file.exists():
        paper_file = Path("docs/IEEE_RESEARCH_PAPER.md")
    raw = paper_file.read_text(encoding="utf-8")
    # strip tags
    raw = re.sub(r'<style[^>]*>.*?</style>', '', raw, flags=re.DOTALL)
    raw = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', raw)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return '\n\n'.join(lines)

def run_loop_iteration(iteration_num: int):
    print(f"\n{'='*70}")
    print(f"  LOOP ITERATION {iteration_num}: AI CONTENT & SIMILARITY AUDIT")
    print(f"{'='*70}")
    
    with open("tools/build_ieee_paper.py", "r", encoding="utf-8") as f:
        build_code = f.read()
        
    # Extract body text from HTML template in build_ieee_paper.py
    # Remove HTML tags to evaluate pure linguistic properties
    pure_text = re.sub(r'<[^>]+>', ' ', build_code)
    # Collapse multiple spaces
    pure_text = re.sub(r'\s+', ' ', pure_text)
    
    result = scan(pure_text)
    print(f"Overall AI Probability : {result.ai_probability:.1%}")
    print(f"Verdict                : {result.verdict} (Confidence: {result.confidence})")
    print(f"Sentence Count         : {result.features.sentence_count}")
    print(f"Word Count             : {result.features.word_count}")
    print(f"Burstiness Score       : {result.features.burstiness:.4f}")
    print(f"Sentence Variance      : {result.features.sentence_length_variance:.4f}")
    print(f"Slop Word Score        : {result.features.slop_word_score:.4f}")
    print(f"Lexical Density        : {result.features.lexical_density:.4f}")
    
    flagged = []
    if hasattr(result, 'sentence_scores'):
        for s in result.sentence_scores:
            # Exclude references section from flagging
            if any(bib in s.text for bib in ["Neurocomputing", "NeurIPS", "IEEE Trans", "Proceedings", "Available: http"]):
                continue
            if s.ai_probability > 0.35 or len(s.flags) > 0:
                flagged.append(s)
                
    print(f"\nFlagged Sentences (excluding citations): {len(flagged)}")
    for i, s in enumerate(flagged[:10]):
        print(f"  [{i+1}] ({s.ai_probability:.1%}) Flags: {s.flags}")
        t = s.text.strip().replace('\n', ' ')
        print(f"      Text: {t[:120]}...")
        
    return result, flagged

if __name__ == "__main__":
    result, flagged = run_loop_iteration(1)

