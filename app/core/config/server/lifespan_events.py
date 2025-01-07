from app.core.di.containers import CoreContainer


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
            "app.core"
        ]
    )
