try:
    from main import app
except:
    from .main import app

# do some production specific things to the app
app.config['DEBUG'] = True


if __name__ == "__main__":
    app.run()