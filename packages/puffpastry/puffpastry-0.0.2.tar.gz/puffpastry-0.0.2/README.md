# :bread: puffpastry

A lightweight, intuitive, Pythonic dependency injection framework.

Highlights:

* :mushroom: Micro framework with very little overhead - single file implementation and handful of public API methods.
* :snake: Compliant with latest Python 3.x versions
* :full_moon: Unit-tests cover all core functionality

## Getting Started

To install from PyPI, use pip:

    pip install puffpastry

The following example shows bootstrapping a webapp using fastapi with configuration read from environment (or from `.env` file, as we use [python-dotenv](https://github.com/theskumar/python-dotenv) under the hood). Of course, for such a minimal one-file implementation, dependency injection seems superfluous; but for larger codebases spread across multiple files this is a great way to manage dependencies and configuration.

```python
from fastapi import FastAPI
from puffpastry import create, provides
from requests import get


class IpifyClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def ipv4(self):
        return get(self.base_url).content.decode("utf8")


@provides("fastapi")
def fastapi_provider(app):
    return FastAPI()


@provides("ipify_client")
def ipify_client(app):
    # The base url will be read from IPIFY_BASE_URL env variable or .env file
    return IpifyClient(base_url=app.config.ipify_base_url)


@provides("home_route")
def home_route_provider(app):
    @app.fastapi.get("/")
    def home():
        public_ip = app.ipify_client.ipv4()

        return {"message": f"your public IP is {public_ip}"}


def create_app():
    return create("my_app").load("fastapi", "ipify_client", "home_route")


app = create_app().fastapi
```

you can run this example with the fastapi CLI, assuming you saved the file as `app.py`:

    fastapi dev app.py

See examples/ for more usage examples.
