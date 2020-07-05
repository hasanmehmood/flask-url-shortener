from urlshort import create_app


def test_shorten(client):
    resp = client.get('/')
    assert b'Shorten' in resp.data

def test_url_shorten_heading(client):
    resp = client.get('/')
    assert b'URL Shortener' in resp.data

def test_page_not_found(client):
    resp = client.get('/somethingnotdefined')
    assert b"We couldn't find what you are looking for. Come vist our homepage :)" in resp.data
