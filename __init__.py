# This is the __init__.py file for the SFM-Graph-Service package.
# It initializes the package and makes its modules importable.

__version__ = "1.0.0"

# Import key modules for convenience
from core import sfm_enums, sfm_models, sfm_query
from db import sfm_dao
from tests import test_sfm_dao, test_sfm_models, test_sfm_models_ext, test_sfm_query
