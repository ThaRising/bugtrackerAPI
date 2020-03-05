from .comment import api as comment_api
from .issue import api as issue_api
from .type import api as type_api
from .user import api as user_api
from webargs import fields, validate


class Collection:
    mask = (lambda k: "*" if not k.get("fields") else ",".join(k.get("fields")))
    query_args = {
        "fields": fields.DelimitedList(fields.Str())
}


from .tag import api as tag_api


__all__ = ["comment_api", "issue_api", "tag_api", "type_api", "user_api"]
