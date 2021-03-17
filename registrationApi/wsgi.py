import registrationapi
app = registrationapi.create_app()


if __name__ == '__main__':
    # Entry point when run via Python interpreter.
    app.run()