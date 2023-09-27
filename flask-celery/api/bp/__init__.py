def create_api_bp(app):

    # existing code omitted

    from . import interface
    app.register_blueprint(interface.testbp)

    return app