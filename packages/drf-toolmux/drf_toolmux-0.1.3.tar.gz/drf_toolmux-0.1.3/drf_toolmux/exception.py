import logging
import threading
import traceback

from rest_framework import status
from rest_framework.exceptions import APIException

from .bot import alert_to_telegram
from .responses import CustomResponse
from .translate import default_error_massage


class RESTException(APIException):

    def __init__(self, status_code=400, detail=None, code=None, **kwargs):
        super().__init__(detail, code)
        self.status_code = status_code
        if not detail:
            self.detail = kwargs


def custom_exception_handler(exc, context):
    request = context.get('request')
    language = request.headers.get("language", "en")
    traceback_ = traceback.format_exc()
    logging.error(traceback_)

    try:
        message = dict(getattr(exc, 'detail', exc))
        error_message = message.get('message', default_error_massage.get(language))
    except Exception as error:
        message = str(getattr(exc, 'detail', exc))
        error_message = default_error_massage.get(language)

    threading.Thread(target=alert_to_telegram, args=[traceback_, message]).start()
    return CustomResponse(
        message=error_message,
        status=getattr(exc, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
    )
