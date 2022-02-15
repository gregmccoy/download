import pytest
from httpx import AsyncClient

from app.main import create_app


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def app(anyio_backend):
    app = create_app()
    yield app


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url='https://') as client:
        yield client
