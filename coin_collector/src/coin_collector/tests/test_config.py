import json
import pytest
from coin_collector.config import load_level, Level

def test_valid_level_loads(tmp_path):
    data = {
        "width": 640, "height": 480,
        "player_start": {"x": 30, "y": 30},
        "coins": [{"x": 100, "y": 100, "r": 10}],
        "walls": []
    }
    p = tmp_path / "ok.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    lvl = load_level(str(p))
    assert isinstance(lvl, Level)
    assert lvl.width == 640
    assert len(lvl.coins) == 1

def test_invalid_level_raises(tmp_path):
    # width als String -> sollte Fehler auslösen
    bad = {
        "width": "breit", "height": 480,
        "player_start": {"x": 30, "y": 30},
        "coins": [{"x": 100, "y": 100, "r": 10}],
        "walls": []
    }
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(Exception):
        load_level(str(p))