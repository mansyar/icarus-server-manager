import pytest
from icarus_sentinel import style_config

def test_style_config_colors():
    assert hasattr(style_config, "APP_BG")
    assert hasattr(style_config, "SIDEBAR_BG")
    assert hasattr(style_config, "FRAME_BG")
    assert hasattr(style_config, "TEXT_PRIMARY")
    assert hasattr(style_config, "ACCENT_COLOR")
    assert hasattr(style_config, "CONSOLE_BG")
    assert hasattr(style_config, "CONSOLE_TEXT")

    # Verify specific hex codes from spec
    assert style_config.APP_BG == "#141414"
    assert style_config.SIDEBAR_BG == "#1A1A1A"
    assert style_config.FRAME_BG == "#2A2A2A"
    assert style_config.TEXT_PRIMARY == "#E0E0E0"
    assert style_config.ACCENT_COLOR == "#FF8C00"
    assert style_config.CONSOLE_BG == "#000000"
    assert style_config.CONSOLE_TEXT == "#FF8C00"

def test_style_config_typography():
    assert hasattr(style_config, "FONT_MAIN")
    assert hasattr(style_config, "FONT_MONO")
    
    assert isinstance(style_config.FONT_MAIN, tuple)
    assert isinstance(style_config.FONT_MONO, tuple)

def test_style_config_geometry():
    assert hasattr(style_config, "CORNER_RADIUS")
    assert style_config.CORNER_RADIUS >= 10
    assert style_config.CORNER_RADIUS <= 15
