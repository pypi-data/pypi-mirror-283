from django.conf import settings

default_error_massage = settings.DEFAULT_ERROR_MASSAGE if hasattr(settings, "DEFAULT_ERROR_MASSAGE") else {
    "en": "Something went wrong. Try again later!",
    'ru': "Что-то пошло не так. Попробуйте позже!"
}
