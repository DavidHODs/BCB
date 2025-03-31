from fastapi import APIRouter
from typing_extensions import Sequence, Tuple

from .app import AppRoute
from .book import BookRoute
from .chat import ChatRoute

app_routes: APIRouter = AppRoute().router
book_routes: APIRouter = BookRoute().router
chat_routes: APIRouter = ChatRoute().router

all_routes: Sequence[Tuple[APIRouter, list[str]]] = [
    (app_routes, ["Health"]),
    (book_routes, ["Book Management"]),
    (chat_routes, ["Chat Management"])
]

__all__ = ["all_routes"]
