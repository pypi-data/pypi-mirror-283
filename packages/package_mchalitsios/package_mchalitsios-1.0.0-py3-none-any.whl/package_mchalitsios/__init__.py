# src/package_mchalitsios/__init__.py
'''
Package-level initialization so users can:
from package_mchalitsios import Observer, Resource
'''
from .telemetry_kit import Observer, Resource

__all__ = ["Observer", "Resource"]
