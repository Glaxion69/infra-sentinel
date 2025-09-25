
from infra_sentinel.engine import load_yaml_files, matches

def test_load_sorted():
    rules = load_yaml_files("rules")
    assert rules[0]["priority"] <= rules[-1]["priority"]
