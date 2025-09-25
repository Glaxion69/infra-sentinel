
import yaml, pathlib

def test_rules_parse():
    for p in pathlib.Path("rules").glob("*.yaml"):
        with open(p, "r", encoding="utf-8") as f:
            assert yaml.safe_load(f) is not None
