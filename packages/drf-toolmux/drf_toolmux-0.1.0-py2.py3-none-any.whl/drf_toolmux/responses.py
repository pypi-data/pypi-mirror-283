import json
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None, **kwargs):
        super(CustomResponse, self).__init__(data, status,
                                             template_name, headers,
                                             exception, content_type, )
        self.data = kwargs if not data else self.data


class RESTException(APIException):

    def __init__(self, status_code=400, detail=None, code=None, **kwargs):
        super().__init__(detail, code)
        self.status_code = status_code
        if not detail:
            self.detail = kwargs


# for web socket
class CustomSocketResponse:
    def __init__(self, status):
        self.status = status

    def __call__(self, **kwargs):
        kwargs['status'] = self.status
        return json.dumps(kwargs)


SocketErrorResponse = CustomSocketResponse(status='error')

SocketSuccessResponse = CustomSocketResponse(status='success')
