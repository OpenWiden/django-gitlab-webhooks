from django.core.signals import Signal

push = Signal(providing_args=["payload"])
tag_push = Signal(providing_args=["payload"])
issue = Signal(providing_args=["payload"])
note = Signal(providing_args=["payload"])
merge_request = Signal(providing_args=["payload"])
wiki_page = Signal(providing_args=["payload"])
pipeline = Signal(providing_args=["payload"])
job = Signal(providing_args=["payload"])
