from . import configs

# Context Default
def Context_Default(request):
    context = {
        # Config
        'Configs':configs
    }
    return context
# End Context Default