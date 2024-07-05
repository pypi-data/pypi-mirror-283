from importlib.metadata import version

def global_vars(request):
    globals = {
        "VERSION": version("salaora")
    }
    return globals
