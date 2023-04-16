try:
    import importlib

    importlib.import_module("binaryninja")
    from .binja_plugin.plugin import plugin_init

    plugin_init()
except ImportError:
    pass
