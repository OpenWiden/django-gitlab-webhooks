from enum import Enum
from typing import List

from django.utils.translation import gettext_lazy as _

# Headers
TOKEN_HEADER = "HTTP_X_GITLAB_TOKEN"
EVENT_HEADER = "HTTP_X_GITLAB_EVENT"


# Error messages
INVALID_HTTP_X_GITLAB_TOKEN = _("Invalid HTTP_X_GITLAB_TOKEN header value.")
EVENT_HEADER_IS_MISSING = _("{name} header is missing").format(name=EVENT_HEADER)
EVENT_IS_NOT_ALLOWED = _("{event} is not allowed event.")


class Events(str, Enum):
    PUSH = "Push Hook"
    TAG_PUSH = "Tag Push Hook"
    ISSUE = "Issue Hook"
    NOTE = "Note Hook"
    MERGE_REQUEST = "Merge Request Hook"
    WIKI_PAGE = "Wiki Page Hook"
    PIPELINE = "Pipeline Hook"
    JOB = "Job Hook"

    @classmethod
    def values(cls) -> List[str]:
        return [event.value for event in cls]
