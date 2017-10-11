# pylint: disable=unused-argument
import os

import pytest
from django.conf import settings


@pytest.fixture(scope="session", autouse=True)
def remove_db_file(request):
    """Remove the test DB file before running any test.

    Note:
        It's to prevent errors when changing Django versions.
    """
    os.remove(settings.DATABASES["default"]["TEST"]["NAME"])