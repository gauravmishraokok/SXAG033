"""FastAPI dependency helpers for MEMORA services."""

from __future__ import annotations

from fastapi import Request


def get_agent(request: Request):
    """Return the application agent service."""
    return request.app.state.agent


def get_quarantine_manager(request: Request):
    """Return the quarantine manager service."""
    return request.app.state.quarantine_mgr


def get_resolution_handler(request: Request):
    """Return the resolution handler service."""
    return request.app.state.resolution_handler


def get_episodic_repo(request: Request):
    """Return the episodic repository service."""
    return request.app.state.episodic_repo


def get_kg_repo(request: Request):
    """Return the graph repository service."""
    return request.app.state.kg_repo


def get_settings(request: Request):
    """Return loaded application settings."""
    return request.app.state.settings
