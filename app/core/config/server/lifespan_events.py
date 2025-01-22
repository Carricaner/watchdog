from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from app.core.config.di.containers import CoreContainer
from app.core.usecase.object.usecases import ObjectUseCase
from app.external.di.containers import ExternalContainer


async def application_start() -> None:
    dependency_injection_init()
    await initialize_watchdog_storage()


def gracefully_shutdown() -> None:
    print("Gracefully Shutdown")


def dependency_injection_init() -> None:
    core_container = CoreContainer()
    external_container = ExternalContainer()
    core_container.user_use_case_adapter.override(
        external_container.user_use_case_adapter
    )
    core_container.object_use_case_adapter.override(
        external_container.object_use_case_adapter
    )
    external_container.wire(
        modules=[__name__],
        packages=[
            "app.entry",
            "app.external"
        ]
    )
    core_container.wire(
        modules=[__name__],
        packages=[
            "app.entry",
            "app.core",
            "app.external"
        ]
    )


@inject
async def initialize_watchdog_storage(object_use_case: ObjectUseCase = Depends(Provide[CoreContainer.object_use_case])):
    await object_use_case.initialize_watchdog_storage()
