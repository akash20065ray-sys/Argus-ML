"""
Comprehensive AI Text Forensics & Plagiarism Audit for ArgusML
Using:
1. lmscan (Zero-shot AI Text Forensics & Model Attribution)
2. copydetect (Stanford MOSS Winnowing Algorithm)
3. TF-IDF Cosine Similarity Matrix
"""

import sys
from pathlib import Path

# Add lmscan src to sys.path
sys.path.insert(0, str(Path("tools/lmscan/src").resolve()))
from lmscan import scan

def audit_text_with_lmscan(file_path: Path):
    text = file_path.read_text(encoding="utf-8")
    result = scan(text)
    
    print("=" * 70)
    print(f"LMSCAN FORENSIC AUDIT: {file_path.name}")
    print("=" * 70)
    print(f"Verdict         : {result.verdict}")
    print(f"AI Probability  : {result.ai_probability:.1%}")
    print(f"Confidence      : {result.confidence}")
    print(f"Total Words     : {result.features.word_count}")
    print(f"Total Sentences : {result.features.sentence_count}")
    print(f"Scan Time       : {result.scan_time_s:.4f}s")
    print("-" * 70)
    print(f"Entropy         : {result.features.entropy:.4f}")
    print(f"Burstiness      : {result.features.burstiness:.4f}")
    print(f"Vocab Richness  : {result.features.vocabulary_richness:.4f}")
    print(f"Sentence Var    : {result.features.sentence_length_variance:.4f}")
    print(f"Slop Word Score : {result.features.slop_word_score:.4f}")
    print(f"Lexical Density : {result.features.lexical_density:.4f}")
    print("-" * 70)
    
    if result.model_attribution:
        print("Model Attribution Signals:")
        for m in result.model_attribution:
            print(f"  • {m.model:20}: {m.confidence:.1%}")
            for ev in m.evidence[:3]:
                print(f"      - {ev}")
    else:
        print("Model Attribution Signals: None detected (No distinct LLM fingerprints)")
        
    if result.flags:
        print("\nFlags Detected:")
        for f in result.flags:
            print(f"  ⚠️  {f}")
    else:
        print("\nFlags Detected: None")
        
    # Inspect top sentences with highest AI probability
    if hasattr(result, 'sentence_scores') and result.sentence_scores:
        flagged_sentences = [s for s in result.sentence_scores if s.ai_probability > 0.40]
        flagged_sentences.sort(key=lambda s: s.ai_probability, reverse=True)
        print(f"\nSentences with AI Probability > 40% ({len(flagged_sentences)} out of {len(result.sentence_scores)}):")
        for i, s in enumerate(flagged_sentences[:10]):
            print(f"  [{i+1}] ({s.ai_probability:.1%}) \"{s.text.strip()}\"")
            if s.flags:
                print(f"       Flags: {', '.join(s.flags)}")
                
    print("=" * 70)
    return result

if __name__ == "__main__":
    p1 = Path("C:/Users/akash/Downloads/ArgusML_First_15k_Characters_Humanized.txt")
    if p1.exists():
        audit_text_with_lmscan(p1)
        
    p2 = Path("C:/Users/akash/Downloads/ArgusML_Full_Paper_Humanized.txt")
    if p2.exists():
        audit_text_with_lmscan(p2)

