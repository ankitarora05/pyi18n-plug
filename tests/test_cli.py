from pyi18n.cli import main


def test_list(capsys):
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    for loc in ("en", "de", "fr", "it", "hi", "ur", "zh"):
        assert loc in out


def test_demo(capsys):
    assert main(["demo"]) == 0
    out = capsys.readouterr().out
    assert "Hello, World!" in out
    assert "Hallo, World!" in out
    assert "नमस्ते" in out


def test_translate_cli(capsys):
    assert main(["translate", "greeting", "-l", "hi", "-p", "name=दुनिया"]) == 0
    assert "नमस्ते" in capsys.readouterr().out


def test_init(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["init", "es"]) == 0
    assert (tmp_path / "es.json").exists()


def test_init_refuses_overwrite(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["init", "es"]) == 0
    assert main(["init", "es"]) == 1


def test_validate_ok(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    main(["init", "en"])
    assert main(["validate", str(tmp_path)]) == 0