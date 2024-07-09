from typing import Literal, TypeVar

ResponseT = TypeVar("ResponseT", bound=Literal["json", "txt"])  # why txt, when text
EndpointsT = TypeVar("EndpointsT", bound=Literal["text", "image", "gif", "stats"])
