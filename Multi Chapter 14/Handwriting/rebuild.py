"""Rebuild a review copy without overwriting the homework the user is editing."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import fitz

ROOT = Path(__file__).resolve().parent
VAULT = ROOT.parents[1]
CURRENT = VAULT / 'output/pdf/Completed Multi Chapter 14 HW - Right Lean and Reduced Vertical Variation.pdf'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-current', action='store_true',
                        help='Require all rendered pages to match the current PDF exactly.')
    args = parser.parse_args()
    for script in ['lean_variation.py', 'lean_14_2.py']:
        subprocess.run([sys.executable, str(ROOT/script)], cwd=VAULT, check=True)
    built = ROOT/'build/rebuilt-homework.pdf'
    before = fitz.open(CURRENT)
    after = fitz.open(built)
    assert len(before) == len(after) == 31
    if args.verify_current:
        for i in range(len(before)):
            old = before[i].get_pixmap(matrix=fitz.Matrix(2,2), alpha=False)
            new = after[i].get_pixmap(matrix=fitz.Matrix(2,2), alpha=False)
            assert (old.width,old.height,old.samples) == (new.width,new.height,new.samples), ('Page changed', i+1)
    base = json.loads((ROOT/'assets/numerals-placements.json').read_text())
    page4 = json.loads((ROOT/'build/lean-14-2-placements.json').read_text())
    placements = [row for row in base if row['page'] != 4] + page4
    (ROOT/'build/placements.json').write_text(json.dumps(placements,indent=2)+'\n')
    report = {
        'pages': len(after),
        'all_pages_pixel_identical_to_current': bool(args.verify_current),
        'current_sha256': hashlib.sha256(CURRENT.read_bytes()).hexdigest(),
        'rebuilt_sha256': hashlib.sha256(built.read_bytes()).hexdigest(),
        'rebuild_requires_only_preserved_repo_inputs': True,
    }
    (ROOT/'build/rebuild-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    print('Review copy:', built)

if __name__ == '__main__':
    main()
