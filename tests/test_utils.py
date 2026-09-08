from utils import clean_price

def test_clean_price():
    assert clean_price("8 019₴") == 8019
    assert clean_price("100₴") == 100