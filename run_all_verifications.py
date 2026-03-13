#!/usr/bin/env python3
"""
Run all paper verifications.

Usage:
    python run_all_verifications.py              # Run all
    python run_all_verifications.py paper1       # Run specific paper
    python run_all_verifications.py --list       # List available papers
"""

import sys
import importlib
import os

# Paper registry: maps paper_id to verification module path
PAPERS = {
    "paper1": "implementations.paper1_baldwin1993.verify",
    "paper2": "implementations.paper2_gou2008.verify",
    "paper3": "implementations.paper3_abbasy2009.verify",
    "paper4": "implementations.paper4_gou2014.verify",
    "paper5": "implementations.paper5_emami2010.verify",
    "paper6": "implementations.paper6_jin2022.verify",
    "paper7": "implementations.paper7_abiri2014.verify",
    "paper8": "implementations.paper8_qi2015.verify",
    "paper9": "implementations.paper9_almunif2019.verify",
    "paper10": "implementations.paper10_xie2015.verify",
    "paper11": "implementations.paper11_ghosh2017.verify",
    # paper12: PDF not available (Mohammadi 2009)
    "paper13": "implementations.paper13_manousakis2012.verify",
    "paper14": "implementations.paper14_ahmed2022.verify",
    "paper15": "implementations.paper15_johnson2020.verify",
    # Advanced: real distribution system
    "crest126": "implementations.advanced_crest126.verify",
}


def run_paper(paper_id: str) -> bool:
    """Run verification for a single paper."""
    if paper_id not in PAPERS:
        print(f"Unknown paper: {paper_id}")
        print(f"Available: {list(PAPERS.keys())}")
        return False

    module_path = PAPERS[paper_id]
    try:
        mod = importlib.import_module(module_path)
        return mod.run_verification()
    except Exception as e:
        print(f"ERROR running {paper_id}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if "--list" in sys.argv:
        print("Available papers:")
        for pid in PAPERS:
            print(f"  {pid}: {PAPERS[pid]}")
        return

    targets = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not targets:
        targets = list(PAPERS.keys())

    results = {}
    for pid in targets:
        print(f"\n{'='*60}")
        print(f"Running: {pid}")
        print(f"{'='*60}\n")
        results[pid] = run_paper(pid)

    # Summary
    print(f"\n{'='*60}")
    print("OVERALL SUMMARY")
    print(f"{'='*60}")
    for pid, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {pid}: {status}")

    n_pass = sum(1 for v in results.values() if v)
    n_total = len(results)
    print(f"\n{n_pass}/{n_total} papers verified successfully.")

    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
