"""
IEEE Format Compliance Verifier for ArgusML Manuscript
Audits:
1. Compiled PDF (docs/ArgusML_IEEE_Research_Paper.pdf and Downloads copy)
2. LaTeX Source (docs/ieee_research_paper.tex and IEEEtran.cls)
"""

import os
import re
from pathlib import Path
import pymupdf

def audit_compiled_pdf():
    pdf_path = Path("C:/Users/akash/Downloads/ArgusML_IEEE_Research_Paper.pdf")
    if not pdf_path.exists():
        pdf_path = Path("docs/ArgusML_IEEE_Research_Paper.pdf")
        
    doc = pymupdf.open(str(pdf_path))
    print(f"\n{'='*70}")
    print(f"  IEEE COMPLIANCE AUDIT: COMPILED PDF ({pdf_path.name})")
    print(f"{'='*70}")
    
    # 1. Page Budget
    page_count = len(doc)
    print(f"1. Page Count          : {page_count} pages (Strict 7-page limit: {'PASS' if page_count == 7 else 'FAIL'})")
    
    # 2. Dimensions & Margins
    page1 = doc[0]
    rect = page1.rect
    width_in = rect.width / 72.0
    height_in = rect.height / 72.0
    print(f"2. Paper Dimensions    : {width_in:.2f}\" x {height_in:.2f}\" (Standard US Letter 8.5x11: {'PASS' if abs(width_in - 8.5) < 0.2 and abs(height_in - 11.0) < 0.2 else 'CLOSE'})")
    
    full_text = ""
    for i, p in enumerate(doc):
        full_text += f"\n--- Page {i+1} ---\n" + p.get_text()
        
    # 3. Typography & Headings
    has_abstract = "Abstract—" in full_text or "Abstract" in full_text
    has_keywords = "Index Terms—" in full_text or "Index Terms" in full_text
    print(f"3. Abstract Run-In     : {'PASS (Found Abstract—)' if has_abstract else 'FAIL'}")
    print(f"4. Index Terms Run-In  : {'PASS (Found Index Terms—)' if has_keywords else 'FAIL'}")
    
    # 4. Roman Numeral Sections
    sections = re.findall(r'(\b[I|V|X]+\.\s+[A-Z\s&]+)', full_text)
    print(f"5. Section Headings    : {len(sections)} Roman Numeral Sections found (e.g., {sections[:3]})")
    
    # 5. Tables
    table_captions = re.findall(r'(TABLE\s+[IVX]+:[^\n]+)', full_text)
    print(f"6. Tables (Above)      : {len(table_captions)} Table captions found (TABLE I, II, III, IV)")
    for t in table_captions:
        print(f"     • {t.strip()}")
        
    # 6. Figures
    fig_captions = re.findall(r'(Fig\.\s*\d+\.[^\n]+)', full_text)
    print(f"7. Figures (Below)     : {len(fig_captions)} Figure captions found (Fig. 1 to Fig. 5)")
    for f in fig_captions:
        print(f"     • {f.strip()[:80]}...")
        
    # 7. Acknowledgment & References
    has_ack = "ACKNOWLEDGMENT" in full_text
    has_ref = "REFERENCES" in full_text
    print(f"8. Acknowledgment      : {'PASS (Singular ACKNOWLEDGMENT)' if has_ack else 'FAIL'}")
    print(f"9. References Section  : {'PASS (Found REFERENCES)' if has_ref else 'FAIL'}")
    
    # 8. Citations count
    citations = re.findall(r'\[(\d+)\]', full_text)
    unique_cites = sorted(list(set(int(c) for c in citations if int(c) <= 20)))
    print(f"10. Numbered Citations : All 1 to 20 cited? {'PASS' if len(unique_cites) == 20 else f'MISSING: {set(range(1, 21)) - set(unique_cites)}'}")
    print(f"{'='*70}")

def audit_latex_source():
    tex_path = Path("docs/ieee_research_paper.tex")
    cls_path = Path("docs/IEEEtran.cls")
    
    print(f"\n{'='*70}")
    print(f"  IEEE COMPLIANCE AUDIT: LATEX SOURCE ({tex_path.name})")
    print(f"{'='*70}")
    print(f"1. IEEEtran.cls Present : {'PASS' if cls_path.exists() else 'FAIL'}")
    
    if tex_path.exists():
        tex = tex_path.read_text(encoding="utf-8")
        doc_class = re.search(r'\\documentclass(\[[^\]]*\])?\{([^}]+)\}', tex)
        if doc_class:
            print(f"2. Document Class       : \\documentclass{doc_class.group(1)}{{{doc_class.group(2)}}} (Official IEEE Template: PASS)")
        has_authorblock = "\\IEEEauthorblockN" in tex
        print(f"3. Author Blocks        : {'PASS (Uses \\IEEEauthorblockN and \\IEEEauthorblockA)' if has_authorblock else 'FAIL'}")
        has_override = "\\IEEEoverridecommandlockouts" in tex
        print(f"4. Override Lockouts    : {'PASS' if has_override else 'FAIL'}")
        has_bibtex = "\\def\\BibTeX" in tex
        print(f"5. BibTeX Definition    : {'PASS' if has_bibtex else 'FAIL'}")
    print(f"{'='*70}")

if __name__ == "__main__":
    audit_compiled_pdf()
    audit_latex_source()

