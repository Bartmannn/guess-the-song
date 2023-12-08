from website.downloader import remove_numbering

def test_remove_numbering():
    assert remove_numbering('aaa30', '30') == 'aaa'