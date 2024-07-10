# src/telempack/__init__.py
'''
Package-level initialization so users can:
from telempack import Observer, Resource
'''
from .opentelemetry_kit import Observer, Resource

__all__ = ["Observer", "Resource"]

#TODO: Initialize logger, etc here.