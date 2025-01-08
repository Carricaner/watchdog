from app.core.config.di.containers import CoreContainer
from app.external.di.containers import ExternalContainer


def application_start() -> None:
    dependency_injection_init()


def gracefully_shutdown() -> None:
    print("Gracefully Shutdown")


def dependency_injection_init() -> None:
    core_container = CoreContainer()
    core_container.wire(
        modules=[__name__],
        packages=[
            "app.entry",
            "app.core",
            "app.external"
        ]
    )

    external_container = ExternalContainer()
    external_container.wire(
        modules=[__name__],
        packages=[
            "app.entry",
            "app.external"
        ]
    )
