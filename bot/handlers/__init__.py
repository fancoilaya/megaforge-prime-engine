# bot/handlers/__init__.py

import pkgutil
import importlib
import logging

def auto_register_handlers(app):
    """
    Automatically import all handler modules in this folder
    and call their register(app) function if present.
    """
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        if module_name.startswith("_"):
            continue

        module = importlib.import_module(f"{__name__}.{module_name}")

        if hasattr(module, "register"):
            logging.info(f"Registering handler: {module_name}")
            module.register(app)

