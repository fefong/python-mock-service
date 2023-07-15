import logging

from flask import Flask


def create_app():
    _app = Flask(__name__)

    # {{ Manager - REST API }}
    from modules.manager.controller import rest_controller
    _app.register_blueprint(rest_controller.rest_blueprint)

    # {{ Mock - REST API }}
    from modules.mock.rest.controller import mock_rest_controller
    _app.register_blueprint(mock_rest_controller.mock_rest_blueprint)

    # # Instance App
    return _app


if __name__ == '__main__':
    logging.root.setLevel(logging.DEBUG)
    app = create_app()

    app.run(host="0.0.0.0", port=5000)
