import logging
from extended_comm.google.service import CreateService
import dotenv

dotenv.load_dotenv()

logging.getLogger('googleapiclient.discovery_cache').setLevel('ERROR')

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())


def _sheet_api():
    sheets = CreateService(api_name='sheets', api_version='v4', scopes=[r'https://www.googleapis.com/auth/spreadsheets'])
    return sheets


# Not Implemented