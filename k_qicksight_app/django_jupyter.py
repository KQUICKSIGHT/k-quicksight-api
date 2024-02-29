# django_jupyter.py

import os
import django

def setup_django(project_root, settings_module):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    django.setup()

    # Add the project root to the Python path. This makes it possible to
    # import your Django apps and models within the Jupyter Notebook.
    import sys
    sys.path.insert(0, project_root)
