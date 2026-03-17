from src.main import main

def test_main_runs(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from Icarus Server Manager!" in captured.out
