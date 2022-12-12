import json

from rest_framework.renderers import JSONRenderer

class UserJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        token = data.get("token", None)
        error = data.get("error", None)

        if error is not None:
            return super(UserJSONRenderer, self).render(data)

        if token and isinstance(token, bytes):
            data["token"] = token.decode(self.charset)

        return json.dumps({"user": data})
