"""
Goal: Main FastAPI application
@authors:
    Gaël MONDON
"""
try:
    import uvicorn

    from fastapi import FastAPI
    from routes.generic import generic_route
    from routes.health import health_route
    from routes.gcp import gcp_route
    from routes.azure import azure_route
    from routes.aws import aws_route

    from config import fast_api_config

except ImportError as error:
    import sys
    sys.exit("Missing required package: {}".format(error))


# The FastAPI web-application object
app = FastAPI(title=fast_api_config['title'],
              version=fast_api_config['version'],
              description=fast_api_config['description'],
              docs_url=fast_api_config['docs_url'],
              redoc_url=fast_api_config['redoc_url'],
              )


# include routes
app.include_router(health_route)
app.include_router(generic_route)
app.include_router(aws_route)
app.include_router(azure_route)
app.include_router(gcp_route)


if __name__ == "__main__":
    uvicorn.run("main:app", headers=[("server", "zabbixwebhook")])
