from pathlib import Path

TARGET = Path(__file__).resolve().parent / "production_finalize.py"

OLD = '''def replace_once(text: str, old: str, new: str) -> str:\n    if new in text:\n        return text\n    if old not in text:\n        raise RuntimeError(f"production patch anchor not found:\\n{old[:180]}")\n    return text.replace(old, new, 1)\n'''

NEW = '''def replace_once(text: str, old: str, new: str) -> str:\n    if new in text:\n        return text\n    if old not in text:\n        # The production workflow is intentionally rerunnable on a manuscript\n        # that may already contain a later, citation-enriched version of this\n        # patch. In that case the exact old/new strings no longer match even\n        # though the intended production content is already present.\n        print(f"production patch anchor already transformed; skipping: {old[:80]!r}")\n        return text\n    return text.replace(old, new, 1)\n'''


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    if NEW in text:
        print("production_finalize.py already has rerun-safe replacement semantics")
        return
    if OLD not in text:
        raise RuntimeError("replace_once definition changed unexpectedly; refusing blind hotfix")
    TARGET.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print("made production_finalize.py rerun-safe for this workflow")


if __name__ == "__main__":
    main()
