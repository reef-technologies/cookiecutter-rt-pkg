# COOKIECUTTER{%- if cookiecutter.is_django_package == "y" -%}
from .django_fixtures import *  # noqa: F401, F403
# COOKIECUTTER{%- endif %}
