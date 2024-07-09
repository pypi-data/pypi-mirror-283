import requests, logging, os, base64, urllib3
from datetime import datetime

logging.basicConfig(filename='log.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def aitAUTH(client_id, client_secret, tenant_id, AIT_Development=False):
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "tenant_id": tenant_id
    }
    headers = {
        "client-id": client_id,
        "client-secret": client_secret,
        "tenant-id": tenant_id
    }

    authentication_dev = "https://aitdev.ari.only.sap/api/token"
    authentication = "https://ait.ari.only.sap/api/token"

    if AIT_Development:
        authentication = authentication_dev

    logging.debug(f'Auth URL: {authentication} / json: {data}')
    access_token_response = requests.post(authentication, json=data, headers=headers)
    logging.debug(f'Response: {access_token_response}')
    if access_token_response.status_code == 200:
        access_token = access_token_response.json()['access_token']
        logging.debug(f'Access Token: {access_token}')
        logging.info('Authentication Successful')
        return access_token_response
    else:
        logging.error(f'{access_token_response.json()}')
        exit()
