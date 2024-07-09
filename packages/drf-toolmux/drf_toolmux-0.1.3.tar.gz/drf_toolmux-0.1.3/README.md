# DRF-TOOLMUX: Django tools collection

![Logo](https://i.ibb.co/frTXGtq/toolmux.png)

![purpose](https://img.shields.io/badge/drfcollection-tools-green)
![PyPI - Version](https://img.shields.io/pypi/v/drf-toolmux)
![License](https://img.shields.io/badge/license-Mirmux-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.9+-brightgreen.svg)
![DRF Version](https://img.shields.io/badge/DRF-3.0+-brightgreen.svg)

## Overview

`drf-toolmux` is a collection of utilities designed to enhance your Django Rest Framework (DRF) projects. This package
provides tools for connecting bots to projects for error reporting, calculating user distances, custom exception
classes, lazy pagination, and custom responses.

## Features

- **Bot Integration for Error Reporting**: Connect your project to a bot to automatically send error notifications.
- **User Distance Calculation**: Utilities to calculate distances between users.
- **Custom Exception Classes**: Enhanced exception handling with custom exceptions.
- **Custom Lazy Pagination**: Efficient pagination for large datasets.
- **Custom Responses**: Simplified and consistent response formatting and socket responses.

## Installation

Install the package using pip:

```shell
pip install drf-toolmux
```

## How to use it

### Default exception:

* settings.py

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'drf_toolmux.exception.custom_exception_handler',
}
```

### Usage custom response

##### You can include any key with a class attribute, and the response will include that key and the corresponding value.

### CustomResponse(custom_key="Test")

* views.py

```python
from rest_framework.views import APIView
from drf_toolmux.responses import CustomResponse


class CreateView(APIView):

    def post(self, request, *args, **kwargs):
        return CustomResponse(message="Response message!")
```

### Usage custom exception class

### RESTException(custom_key="Test")

* views.py

```python
from rest_framework.views import APIView
from drf_toolmux.exception import RESTException


class CreateView(APIView):

    def post(self, request, *args, **kwargs):
        raise RESTException(message="Error message!")
```

### Usage Lazy Scroll Pagination and PaginationView

This pagination class provides a ready-to-use solution for simple view pagination. It supports lazy scrolling by
providing the next and previous values as integers for seamless navigation.

```python
from rest_framework.views import APIView
from drf_toolmux.pagination import PaginationView


class View(PaginationView, APIView):
    pass
```

```python
from rest_framework.generics import ListAPIView
from drf_toolmux.pagination import MyPagination


class View(ListAPIView):
    pagination_class = MyPagination
```

The results will be like this:

```json
{
  "next": 3,
  "previous": 1,
  "page_size": 10,
  "count": 1,
  "total_pages": 3,
  "results": []
}
```

### Socket Pagination Response

```python
from drf_toolmux.pagination import SocketPaginationView


class ChatPrivateRoom(SocketPaginationView):

    def get_private_chat_list(self, *args, **kwargs):
        return self.send_pagination_response(queryset="queryset should be", serializer="serializer class",
                                             action="any action that you want")
```

Results will be like this:

```json
{
  "action": "any action that you sent",
  "next": 3,
  "previous": 1,
  "current_page": 2,
  "page_size": 20,
  "count": 3,
  "total_pages": 3,
  "status": "success",
  "results": []
}
```

## Find distance between two users:

```python
from drf_toolmux.distance import define_distance

distance = define_distance(user1={"lat": "", "lng": ""}, user2={"lat": "", "lng": ""}, unit='km')
```