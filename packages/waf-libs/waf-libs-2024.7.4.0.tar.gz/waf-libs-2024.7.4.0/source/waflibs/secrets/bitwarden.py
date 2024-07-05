import bitwarden_sdk

from waflibs import log

"""
bitwarden secrets manager
"""

logger = log.logger().get_logger()

API_URL = "https://api.bitwarden.com"
IDENTITY_URL = "https://identity.bitwarden.com"


class client:
    def __init__(
        self, access_token, org_id, api_url=API_URL, identity_url=IDENTITY_URL
    ):
        logger.debug(f"api url: {api_url}")
        logger.debug(f"identity url: {identity_url}")

        self.org_id = org_id
        self.client = bitwarden_sdk.BitwardenClient(
            bitwarden_sdk.client_settings_from_dict(
                {
                    "apiUrl": api_url,
                    "deviceType": bitwarden_sdk.DeviceType.SDK,
                    "identityUrl": identity_url,
                    "userAgent": "waflibs Python",
                }
            )
        )

        self.client.access_token_login(access_token)

    def get_secret(self, secret_name):
        logger.debug(f"secret name: {secret_name}")

        secrets = self.client.secrets().list(self.org_id).data.to_dict()
        logger.debug(f"all secrets: {secrets}")
        for secret in secrets["data"]:
            if secret["key"] == secret_name:
                logger.debug(f"secret to return: {secret}")

                secret_obj = self.client.secrets().get(secret["id"])
                logger.debug(f"secret object: {secret_obj}")
                return secret_obj.data.value
