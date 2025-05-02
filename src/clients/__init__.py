from core import settings
from ml_http import auto_client

data_client = auto_client(settings.HTTP_DATA_SERVER).http()
query_client = auto_client(settings.HTTP_QUERY_SERVER).http()

