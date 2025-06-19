# This is the __init__.py file for the SFM-Graph-Service package.
# It initializes the package and makes its modules importable.

__version__ = "1.0.0"

# Import key modules for convenience
from core import sfm_models, enums, sfm_query
from db import sfm_dao
from tests import sfm_dao_test, sfm_models_test, sfm_query_test
