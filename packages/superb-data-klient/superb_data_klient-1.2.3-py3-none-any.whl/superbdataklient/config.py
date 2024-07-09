_ACCESS_TOKEN_ENV_KEY = 'SDK_ACCESS_TOKEN'
_REFRESH_TOKEN_ENV_KEY = 'SDK_REFRESH_TOKEN'


class Environment:
    def __init__(self, **kwargs: str):
        self.domain = kwargs.get('domain')
        self.realm = kwargs.get('realm')
        self.client_id = kwargs.get('client_id')
        self.api_version = kwargs.get('api_version')
        self.org_endpoint = f'https://{self.domain}/organizationmanager/api/{self.api_version}/organization'
        self.space_endpoint = f'https://{self.domain}/organizationmanager/api/{self.api_version}/space'
        self.accessmanager_url = f'https://{self.domain}/accessmanager/api/v2.0/accessmanager/'


_ENVS = {
    'sdk': Environment(
            domain='app.sdk-cloud.de',
            realm='efs-sdk',
            client_id='sdk-cli',
            api_version='v1.0',
    ),
    'sdk-dev': Environment(
            domain='dev.sdk-cloud.de',
            realm='efs-sdk',
            client_id='sdk-cli',
            api_version='v1.0',
    ),
}
