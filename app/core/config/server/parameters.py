from app.core.config.server.lifespans import default_lifespan

api_doc_version = "v1"

tags_metadata = [
    {
        "name": "user"
    },
    {
        "name": "object",
        "description": "The object that a user wanna to secure",
    }
]

# All should be rewritten using Pydantic's BaseModel
_404_not_found_response = {
    'description': 'Not found'
}

http_status_to_response_map = {
    404: _404_not_found_response
}

main_router_parameters = {
    "prefix": f"/{api_doc_version}/api",
    "responses": http_status_to_response_map
}

fastapi_api_document_parameters = {
    "title": "Watchdog API Documentation",
    "version": api_doc_version,
    "openapi_tags": tags_metadata,
    "docs_url": f"/{api_doc_version}/doc/swagger",
    "redoc_url": f"/{api_doc_version}/doc/redoc",
}

fastapi_parameters = {
    **fastapi_api_document_parameters,
    "lifespan": default_lifespan
}

__all__ = [
    "fastapi_parameters",
    "main_router_parameters"
]
