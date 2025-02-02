# Watchdog [![CircleCI](https://dl.circleci.com/status-badge/img/circleci/ME2opz6NQmyqhFno6cPKqT/V1gLZ1QzgoFhKGem6FCham/tree/main.svg?style=svg&circle-token=CCIPRJ_YJm16UpjLz2RehZWqxL7rS_85e497af218d7ffc43d94de905224bff20b076a3)](https://dl.circleci.com/status-badge/redirect/circleci/ME2opz6NQmyqhFno6cPKqT/V1gLZ1QzgoFhKGem6FCham/tree/main)

## Description

This project enables users to upload files and make them accessible for a specified period using Python, FastAPI,
CircleCI, MongoDB, and AWS S3. Authenticated users can set expiration times for the generated URLs of their uploaded
files, making it suitable for commercial campaigns and various other scenarios.

## Features

### Concept of Clean Architecture

The whole project is designed under the concept of clean architecture and divided into two parts
including: `Core` & `External`, as below.

- `Core`
    - the most important part of the project
    - includes:
        - `Domain`: most important entities in the whole project
        - `Config`
        - `Use case`
    - must not reply on `External`
    - must communicate with `External` through `Interface`
    - needs unit tests
    - in this way, we can extract `Core` part and place it elsewhere with ease, which makes microservices possible.
- `External`
    - responsible for communicating with the outside world
    - includes:
        - `Entry`: deals with incoming requests, like HTTP requests.
        - `Adapter` sends commands to or gets data from the outside world, like upload a file to AWS
          S3. Here, I name it as `external` in the project.
    - able to use everything in `Core`

<img src="https://the-general.s3.ap-northeast-1.amazonaws.com/project/redis-impl.svg" width="500" alt="my clean architecture design"/>

## Uses Dependency Injection (DI)

- Adopts DI concept with Dependency Injectors and FastAPI.
- Prepares all necessary components in containers prior to the application's startup, like
    ```python
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
    ```
  and uses it in every place that needs it like
    ```python
    @router.get("/file/all")
    @inject
    async def get_all_file_names(
            current_user: User = Depends(get_current_user),
            object_use_case: ObjectUseCase = Depends(Provide[CoreContainer.object_use_case])
    ):
        return await object_use_case.get_all_user_files(current_user)
    ```

### Used Circle CI, AWS ECR & ECS to test and deploy the project

- the flow is like:
    ```mermaid
    flowchart LR
    test --> B[build and push Docker image] --> deploy[pull the image & deploy to AWS ECS]
    ```

- Benefits of using AWS ECS:
    - It is convenient and easy to use Fargate instances for our app because AWS helps me provision the instances.
    - Auto-scaling can be simply done by specifying hoe many containers I want under whatever circumstances.

## Steps

1. Fill the needed information under `./env/dev/.env` and the format is like:

   ```
    server_mode=dev
    
    authentication__secret_key=6abe695305d7d814b0292c98fac3d5753dcb66bfa7b42941813782f8b3cdad34
    authentication__algorithm=HS256
    authentication__expiration_period=1440
    
    mongodb__connection_url=
    mongodb__database=dev
    
    aws__access_key=
    aws__secret_key=
    aws__region=
   ```

2. Build the Docker image

   ```shell
   docker build -t watchdog .
   ```
3. Run the app

   ```shell
   docker run -d -p 8000:80 --name watchdog-container watchdog
   ```
   
4. Now, we can use the app through `http://localhost:8000`.

## Other Notes

- Remember to install `setuptools` so that IDE can resolve the packages.

## Future Work

## References

- [Awesome FastAPI](https://github.com/mjhea0/awesome-fastapi?tab=readme-ov-file#admin)

