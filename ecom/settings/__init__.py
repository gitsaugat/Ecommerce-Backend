import os
from django.core.exceptions import ImproperlyConfigured

mode = os.environ.get('MODE')

if not mode:
    raise ImproperlyConfigured('No mode specified for project')
if mode == "dev":
    from .dev import *
elif mode == "prod":
    from .prod import *
else:
    raise ImproperlyConfigured('Specify MODE in env_web file, that in which mode you are starting the project'
                               ' development/production mode')
