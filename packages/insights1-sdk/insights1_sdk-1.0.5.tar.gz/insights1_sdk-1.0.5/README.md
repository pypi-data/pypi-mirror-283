
# Getting Started with EPIC Insights APIs

## Introduction

OpenAPI doc for EPIC PI

## Install the Package

The package is compatible with Python versions `3 >=3.7, <= 3.11`.
Install the package from PyPi using the following pip command:

```python
pip install insights1-sdk==1.0.5
```

You can also view the package at:
https://pypi.python.org/pypi/insights1-sdk/1.0.5

## Test the SDK

You can test the generated SDK and the server with test cases. `unittest` is used as the testing framework and `pytest` is used as the test runner. You can run the tests as follows:

Navigate to the root directory of the SDK and run the following commands

```
pip install -r test-requirements.txt
pytest
```

## Initialize the API Client

**_Note:_** Documentation for the client can be found [here.](https://www.github.com/vsvinav/insights-python-sdk/tree/1.0.5/doc/client.md)

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| `default_host` | `str` | *Default*: `'www.example.com'` |
| `environment` | `Environment` | The API environment. <br> **Default: `Environment.PRODUCTION`** |
| `http_client_instance` | `HttpClient` | The Http Client passed from the sdk user for making requests |
| `override_http_client_configuration` | `bool` | The value which determines to override properties of the passed Http Client from the sdk user |
| `http_call_back` | `HttpCallBack` | The callback value that is invoked before and after an HTTP call is made to an endpoint |
| `timeout` | `float` | The value to use for connection timeout. <br> **Default: 60** |
| `max_retries` | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| `backoff_factor` | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 2** |
| `retry_statuses` | `Array of int` | The http statuses on which retry is to be done. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| `retry_methods` | `Array of string` | The http methods on which retry is to be done. <br> **Default: ['GET', 'PUT']** |
| `skip_ssl_cert_verification` | `boolean` | Set to true to allow skipping ssl certificate verification |
| `custom_header_authentication_credentials` | [`CustomHeaderAuthenticationCredentials`](https://www.github.com/vsvinav/insights-python-sdk/tree/1.0.5/doc/$a/https://www.github.com/vsvinav/insights-python-sdk/tree/1.0.5/custom-header-signature.md) | The credential object for Custom Header Signature |

The API client can be initialized as follows:

```python
client = EpicinsightsapisClient(
    custom_header_authentication_credentials=CustomHeaderAuthenticationCredentials(
        authorization='Authorization'
    ),
    default_host='www.example.com'
)
```

## Authorization

This API uses the following authentication schemes.

* [`APIKeyHeader (Custom Header Signature)`](https://www.github.com/vsvinav/insights-python-sdk/tree/1.0.5/doc/$a/https://www.github.com/vsvinav/insights-python-sdk/tree/1.0.5/custom-header-signature.md)

## List of APIs

* [TSDB Query](https://www.github.com/vsvinav/insights-python-sdk/tree/1.0.5/doc/controllers/tsdb-query.md)
* [Health](https://www.github.com/vsvinav/insights-python-sdk/tree/1.0.5/doc/controllers/health.md)
* [Alerta](https://www.github.com/vsvinav/insights-python-sdk/tree/1.0.5/doc/controllers/alerta.md)

## Classes Documentation

* [Utility Classes](https://www.github.com/vsvinav/insights-python-sdk/tree/1.0.5/doc/utility-classes.md)
* [HttpResponse](https://www.github.com/vsvinav/insights-python-sdk/tree/1.0.5/doc/http-response.md)
* [HttpRequest](https://www.github.com/vsvinav/insights-python-sdk/tree/1.0.5/doc/http-request.md)

