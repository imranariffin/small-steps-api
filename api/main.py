from os import environ
from typing import Dict, List

from fastapi import FastAPI

from goals.routing import router as goals_router

api = FastAPI()


@api.get("/")
def root():
    def get_base_url() -> str:
        return f"http://{environ['API_HOST']}:{environ['API_PORT']}"

    def get_routes_map(routes: List) -> Dict[str, str]:
        return {
            route.name: f"{get_base_url()}{route.path}"
            for route in routes
        }

    return get_routes_map(api.routes)


api.include_router(prefix="/goals", router=goals_router)
