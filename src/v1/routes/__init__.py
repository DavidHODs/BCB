from fastapi import APIRouter
from typing_extensions import Sequence, Tuple

from .app import AppRoutes

app_routes: APIRouter = AppRoutes().router

all_routes: Sequence[Tuple[APIRouter, list[str]]] = [
    (app_routes, ["Health"])
]

__all__ = ["all_routes"]
