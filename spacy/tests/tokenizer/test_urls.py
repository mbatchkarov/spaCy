from __future__ import unicode_literals

import pytest

URLS = [
    u"http://www.nytimes.com/2016/04/20/us/politics/new-york-primary-preview.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=a-lede-package-region&region=top-news&WT.nav=top-news&_r=0",
    u"www.google.com?q=google",
    u"google.com",
    u"www.red-stars.com",
    pytest.mark.xfail(u"red-stars.com"),
    u"http://foo.com/blah_(wikipedia)#cite-1",
    u"http://www.example.com/wpstyle/?bar=baz&inga=42&quux",
    u"mailto:foo.bar@baz.com",
    u"mailto:foo-bar@baz-co.com"
]

# Punctuation we want to check is split away before the URL
PREFIXES = [
    "(", '"', "...",  ">"
]

# Punctuation we want to check is split away after the URL
SUFFIXES = [
    '"', ":", ">"]

@pytest.mark.parametrize("text", URLS)
def test_simple_url(tokenizer, text):
    tokens = tokenizer(text)
    assert tokens[0].orth_ == text
    assert len(tokens) == 1


@pytest.mark.parametrize("prefix", PREFIXES)
@pytest.mark.parametrize("url", URLS)
def test_prefixed_url(tokenizer, prefix, url):
    tokens = tokenizer(prefix + url)
    assert tokens[0].text == prefix
    assert tokens[1].text == url
    assert len(tokens) == 2
    
@pytest.mark.parametrize("suffix", SUFFIXES)
@pytest.mark.parametrize("url", URLS)
def test_suffixed_url(tokenizer, url, suffix):
    tokens = tokenizer(url + suffix)
    assert tokens[0].text == url
    assert tokens[1].text == suffix
    assert len(tokens) == 2
    
@pytest.mark.parametrize("prefix", PREFIXES)
@pytest.mark.parametrize("suffix", SUFFIXES)
@pytest.mark.parametrize("url", URLS)
def test_surround_url(tokenizer, prefix, suffix, url):
    tokens = tokenizer(prefix + url + suffix)
    assert tokens[0].text == prefix
    assert tokens[1].text == url
    assert tokens[2].text == suffix
    assert len(tokens) == 3
    
@pytest.mark.parametrize("prefix1", PREFIXES)
@pytest.mark.parametrize("prefix2", PREFIXES)
@pytest.mark.parametrize("url", URLS)
def test_two_prefix_url(tokenizer, prefix1, prefix2, url):
    tokens = tokenizer(prefix1 + prefix2 + url)
    assert tokens[0].text == prefix1
    assert tokens[1].text == prefix2
    assert tokens[2].text == url
    assert len(tokens) == 3
    
@pytest.mark.parametrize("suffix1", SUFFIXES)
@pytest.mark.parametrize("suffix2", SUFFIXES)
@pytest.mark.parametrize("url", URLS)
def test_two_prefix_url(tokenizer, suffix1, suffix2, url):
    tokens = tokenizer(url + suffix1 + suffix2)
    assert tokens[0].text == url
    assert tokens[1].text == suffix1
    assert tokens[2].text == suffix2
    assert len(tokens) == 3
