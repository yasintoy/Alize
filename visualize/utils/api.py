from functools import partial

import requests
from urllib.parse import urljoin
from django.conf import settings


def _make_request(url, cls, method='GET', params=None, url_params=None, **kwargs):
    """ 
    @params url: request url
    @params method: request type (GET, POST, PUT, DELETE)
    @params params: querystring
    @params url_params: Dynamic url params.
            for example: url, /users/%(username)/, url_params, {'username': "yasintoy"}
    """
    headers= {
        'Content-Type': 'application/json',
        'Authorization': 'token %s' % settings.API_TOKEN
    }
    if url_params:
        url = url.format(**url_params)

    response = requests.request(url=url, method=method,
                                params=params, headers=headers, **kwargs)
    return response.json()


class Client(object):
    """
    Usage:
        >> Client().user_info(access_token='a')
        >> Client().user_repo_info(access_token='a')
    """
    _endpoints = {
        'user_info': 'users/{username}',
        'user_repo_info': 'users/{username}/repos'
    }

    def __getattr__(self, name):
        if name not in self._endpoints.keys():
            raise AttributeError(name)

        url = self._endpoints[name]
        return partial(
            _make_request,
            url=urljoin(settings.API_BASE, url),
            cls=self
        )

