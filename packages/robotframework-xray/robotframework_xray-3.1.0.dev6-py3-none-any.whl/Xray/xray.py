import logging
import json, requests
from ntpath import join
from datetime import datetime
from .config import Config

logger = logging.getLogger(__name__)

class Xray:
    '''
    Classe responsável pela comunicação com a API do X-Ray.
    Documentação oficial: https://docs.getxray.app/display/XRAY/v2.0.
    '''

    XRAY_API : str = Config.xray_api()
    PROJECT_KEY : str = Config.project_key()
    

    def authentication(self) -> str:
        '''
        Realiza a autenticação na API e retorna o token que deve 
        ser utilizado nas outras requisições.
        '''
        XRAY_CLIENT_ID = Config.xray_client_id()
        XRAY_CLIENT_SECRET = Config.xray_client_secret()

        json_data = json.dumps({'client_id': XRAY_CLIENT_ID, 'client_secret': XRAY_CLIENT_SECRET})
        resp = requests.post(f'{self.XRAY_API}/authenticate', data=json_data, headers={'Content-Type':'application/json'})
            
        if resp.status_code == 200:
            print("Authentication successfully!")
            return f'Bearer {resp.json()}'
        else:
            logger.error('Authentication error: ', resp.status_code)


    def createTestExecution(self):
        test_execution_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        json_data = {
            "summary": "Execução automática do Robot",
            "startDate": test_execution_date
        }
        print(json_data)
        response = requests.post(
            f'{self.XRAY_API}/import/execution',
            json={ 'info': json_data },
            headers={
                'Content-Type': 'application/json',
                'Authorization': self.authentication()
            },
        )
        print(response)
        result = json.dumps({
            'issueId': response.json().get('data').get('createTestExecution').get('testExecution').get('issueId'),
            'key': response.json().get('data').get('createTestExecution').get('testExecution').get('jira').get('key')
        })

        if response.status_code == 200:
            print('Created new test execution: ', result['key'])
            return json.loads(result)
        else:
            logger.error('Error create test execution: ', response.json())
    
