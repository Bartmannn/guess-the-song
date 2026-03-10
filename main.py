from website import create_app
from website.consts import (
    ALLOW_UNSAFE_WERKZEUG,
    DEBUG,
    HOST_ADDR,
    HOST_PORT,
    USE_SSL,
)


def main() -> None:
    socketio, app = create_app()

    run_options = {
        "debug": DEBUG,
        "host": HOST_ADDR,
        "port": HOST_PORT,
        "allow_unsafe_werkzeug": ALLOW_UNSAFE_WERKZEUG,
    }
    if USE_SSL:
        run_options["ssl_context"] = "adhoc"

    socketio.run(app, **run_options)


if __name__ == "__main__":
    main()
