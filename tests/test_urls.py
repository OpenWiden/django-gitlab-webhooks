from django.urls import resolve, reverse


def test_receive_url():
    namespace = "receive"
    url = "/receive/"

    assert reverse(namespace) == url
    assert resolve(url).view_name == namespace
