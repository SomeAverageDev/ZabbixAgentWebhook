"""
Goal: Main Flask application
@authors:
    Gaël MONDON
"""
try:
    from flask import Flask
    from routes.health import health_route
    from routes.sitemap import sitemap_route
    from routes.help import help_route
    from routes.generic import generic_route
    from routes.azure import azure_route
    from routes.gcp import gcp_route
    from routes.aws import aws_route

except ImportError:
    try:
        from .routes.health import health_route
        from .routes.sitemap import sitemap_route
        from .routes.help import help_route
        from .routes.generic import generic_route
        from .routes.azure import azure_route
        from .routes.gcp import gcp_route
        from .routes.aws import aws_route
    except ImportError as error:
        import sys
        sys.exit("Missing required package: {}".format(error))


# The WSGI compliant web-application object
app = Flask(__name__)
# add routes
app.register_blueprint(health_route)
app.register_blueprint(help_route)
app.register_blueprint(generic_route)
app.register_blueprint(azure_route)
app.register_blueprint(gcp_route)
app.register_blueprint(aws_route)


if __name__ == "__main__":
    app.run()
