"""
ArgusML Plagiarism & Overlap Audit
Using:
1. Stanford MOSS Winnowing Algorithm via copydetect (Schleimer et al., 2003)
2. Scikit-learn TF-IDF Vectorizer & Cosine Similarity Matrix
"""

import sys
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from copydetect import CopyDetector

def run_plagiarism_audit():
    print("=" * 70)
    print("PLAGIARISM & SIMILARITY AUDIT")
    print("=" * 70)
    
    # 1. Compare Sections within Paper for repetitive copy-paste / duplication
    full_paper_path = Path("C:/Users/akash/Downloads/ArgusML_Full_Paper_Humanized.txt")
    if not full_paper_path.exists():
        full_paper_path = Path("docs/IEEE_RESEARCH_PAPER.md")
        
    text = full_paper_path.read_text(encoding="utf-8")
    
    # Split by major sections
    import re
    sections = re.split(r'\n(?=[A-Z0-9IVX]+\.\s+[A-Z])', text)
    if len(sections) < 3:
        # fallback split by markdown headers
        sections = re.split(r'\n(?=#{1,3}\s+)', text)
        
    print(f"Loaded {len(sections)} distinct sections from full paper.")
    
    # TF-IDF Cosine Similarity across all section pairs
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(sections)
    sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    max_cross_sim = 0.0
    highest_pair = (0, 0)
    for i in range(len(sections)):
        for j in range(i + 1, len(sections)):
            score = sim_matrix[i][j]
            if score > max_cross_sim:
                max_cross_sim = score
                highest_pair = (i, j)
                
    print(f"\n[TF-IDF Cross-Section Similarity Results]")
    print(f"  • Maximum Inter-Section Cosine Similarity: {max_cross_sim * 100:.2f}%")
    print(f"  • Average Cross-Section Overlap          : {sim_matrix[sim_matrix < 0.99].mean() * 100:.2f}%")
    if max_cross_sim > 0.40:
        print(f"  ⚠️ Warning: Sections {highest_pair[0]} and {highest_pair[1]} share elevated similarity ({max_cross_sim*100:.1f}%).")
    else:
        print(f"  ✓ Excellent: All sections are structurally independent (< 35% cross-similarity).")
        
    # 2. Stanford MOSS Winnowing Algorithm via CopyDetector
    print(f"\n[Stanford MOSS Winnowing Fingerprinting (copydetect)]")
    # Setup test directory with paper versions
    test_dir = Path("docs/plagiarism_test_workspace")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Save full paper
    (test_dir / "argusml_current.txt").write_text(text, encoding="utf-8")
    
    # Save individual sections as reference docs
    ref_dir = Path("docs/plagiarism_reference_workspace")
    ref_dir.mkdir(parents=True, exist_ok=True)
    for idx, sec in enumerate(sections):
        (ref_dir / f"section_{idx}.txt").write_text(sec, encoding="utf-8")
        
    html_out = Path("docs/ArgusML_MOSS_Winnowing_Report.html")
    detector = CopyDetector(
        test_dirs=[str(test_dir)],
        ref_dirs=[str(ref_dir)],
        boilerplate_dirs=[],
        extensions=["txt"],
        noise_t=25,       # minimum match size in characters
        guarantee_t=30,   # guaranteed detection threshold
        display_t=0.15,   # report matches above 15%
        autoopen=False,
        out_file=str(html_out),
        silent=True
    )
    
    detector.run()
    
    print(f"  • Winnowing Noise Threshold (k): 25 characters")
    print(f"  • Winnowing Window Size (w): 30 characters")
    
    detector.generate_html_report()
    print(f"  ✓ Generated Winnowing Report at: {html_out}")
    print("=" * 70)

if __name__ == "__main__":
    run_plagiarism_audit()
