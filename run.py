import uvicorn

from app.config import ConfigClass
from app.main import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('run:app', host=ConfigClass.host, port=ConfigClass.port, log_level='info', reload=True)
