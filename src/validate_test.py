from validate import is_valid_title

def test_普通のタイトルは_true():
    assert is_valid_title("牛乳を買う") is True

def test_空文字は_false():
    assert is_valid_title("") is False

def test_空白だけは_false():
    assert is_valid_title("   ") is False

def test_100文字を超えると_false():
    long_title = "あ" * 101
    assert is_valid_title(long_title) is False

def test_100文字ちょうどは_true():
    max_title = "あ" * 100
    assert is_valid_title(max_title) is True