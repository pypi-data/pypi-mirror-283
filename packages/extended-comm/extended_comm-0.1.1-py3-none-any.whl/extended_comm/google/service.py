# https://learndataanalysis.org/how-to-use-gmail-api-to-send-an-email-in-python/

import logging
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import json
from pathlib import Path

logger = logging.getLogger(__name__)


def CreateService(api_name, api_version, scopes):
    cred = None

    pickle_file = Path(os.getenv('CREDENTIAL_DIR')) / f'{api_name.lower()}_token.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            config = json.loads(os.getenv('GOOGLE_BOT_SECRET'))
            flow = InstalledAppFlow.from_client_config(config, scopes)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_name, api_version, credentials=cred)
        logger.debug(api_name, 'service created successfully')
        return service
    except Exception as e:
        logger.error(f'Unable to connect!\n{e}')
        return None
