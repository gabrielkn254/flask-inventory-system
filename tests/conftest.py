import pytest
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)

    with app.test_client() as client:
        yield client