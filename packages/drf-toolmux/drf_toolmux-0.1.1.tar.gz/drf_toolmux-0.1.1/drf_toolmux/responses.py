import json
from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None, **kwargs):
        super(CustomResponse, self).__init__(data, status,
                                             template_name, headers,
                                             exception, content_type, )
        self.data = kwargs if not data else self.data


# for web socket
class CustomSocketResponse:
    def __init__(self, status):
        self.status = status

    def __call__(self, **kwargs):
        kwargs['status'] = self.status
        return json.dumps(kwargs)


SocketErrorResponse = CustomSocketResponse(status='error')

SocketSuccessResponse = CustomSocketResponse(status='success')
