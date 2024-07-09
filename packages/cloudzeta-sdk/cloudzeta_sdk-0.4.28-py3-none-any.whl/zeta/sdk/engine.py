from __future__ import annotations
from cryptography.fernet import Fernet
from google.cloud import firestore
from google.oauth2 import credentials
from enum import Enum
import os
import requests

from zeta.utils.logging import zetaLogger

CLOUD_ZETA_PROJECT_ID = "gozeta-prod"
CLOUD_ZETA_API_KEY = "AIzaSyBBDfxgpOAnH7GJ6RNu0Q_v79OGbVr1V2Q"
CLOUD_ZETA_URL_PREFIX = "https://cloudzeta.com"
GOOGLE_AUTH_URL = "https://securetoken.googleapis.com/v1/token"


class ZetaUploadResult(object):
    class Status(Enum):
        INVALID = 0
        PENDING = 1
        SUCCESS = 2
        FAILURE = 3

    def __init__(self):
        self.status: ZetaUploadResult.Status = ZetaUploadResult.Status.INVALID
        self.asset_path: str = None
        self.blob_path: str = None
        self._error: str = None

    def __str__(self):
        if self.success:
            return "success"
        elif self.error:
            return f"error: {self.error}"
        else:
            return "pending"

    @property
    def success(self) -> bool:
        return self.status == ZetaUploadResult.Status.SUCCESS

    def set_success(self):
        self.status = ZetaUploadResult.Status.SUCCESS
        return self

    @property
    def error(self) -> str:
        return self._error

    def set_error(self, message: str) -> ZetaUploadResult:
        self._error = message
        self.status = ZetaUploadResult.Status.FAILURE
        return self


class ZetaEngine(object):
    def __init__(self, api_key=CLOUD_ZETA_API_KEY, zeta_url_prefix=CLOUD_ZETA_URL_PREFIX):
        self._api_key = api_key
        self._zeta_url_prefix = zeta_url_prefix

        self._auth_token = None
        self._refresh_token = None
        self._user_uid = None

        self._db: firestore.Client = None

    def login(self, token_uid: str, encryption_key: str) -> bool:
        """
        Login with the given token_uid and encryption_key.

        @param token_uid: The token_uid to login with.
        @param encryption_key: The encryption_key to decrypt the token with.
        """
        zeta_auth_token_url = f"{self._zeta_url_prefix}/api/auth/token/get"
        response = requests.get(zeta_auth_token_url, params={"authToken": token_uid})
        if not response.ok:
            zetaLogger.error(f"Failed to get auth token")
            return False

        res = response.json()
        encrypted_token = res.get("encryptedToken")

        try:
            fernet = Fernet(encryption_key.encode())
            self._refresh_token = fernet.decrypt(encrypted_token.encode()).decode()
        except Exception as e:
            zetaLogger.error("Failed to decrypt token.")
            return False

        google_login_url = f"{GOOGLE_AUTH_URL}?key={self._api_key}"
        response = requests.post(
            google_login_url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            }, data={
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
            }
        )

        if not response.ok:
            zetaLogger.error(f"Failed to login with auth token")
            return False

        res = response.json()
        self._auth_token = res["id_token"]
        self._refresh_token = res["refresh_token"]
        self._user_uid = res["user_id"]

        assert self._auth_token is not None
        assert self._refresh_token is not None
        assert self._user_uid is not None

        cred = credentials.Credentials(
            self._auth_token, self._refresh_token, client_id="", client_secret="",
            token_uri=f"{GOOGLE_AUTH_URL}?key={self._api_key}")

        self._db = firestore.Client(CLOUD_ZETA_PROJECT_ID, cred)
        assert self._db is not None

        return True

    def upload_asset(self,
                     owner_name: str,
                     project_name: str,
                     asset_path: str,
                     data) -> ZetaUploadResult:
        """
        Upload the asset to the given owner_name and project_name. The server will validate:
        1. The traget project exists
        2. The user has the permission to upload the asset
        3. There is no asset with the same name in the project

        @param owner_name: The owner_name of the project. Note that the owner can be different than
            the current user, as long as the current user has the permission to upload.
        @param project_name: The project_name to upload the asset to.
        @param asset_path: The path to the asset to upload, relative to the project root. A leading
            "/" for the path is not required and will be ignored.
        @param data: The data to upload.

        @return: The signed URL to the uploaded asset.

        Zeta URL schema: https://cloudzeta.com/<owner_name>/<project_name>/asset/main/<asset_path>

        Example: https://cloudzeta.com/zeta/public-demo/asset/main/zeta-logo.usd
            owner_name: zeta
            project_name: public-demo
            asset_path: zeta-logo.usd
        """
        result = ZetaUploadResult()

        response = requests.post(
            f"{self._zeta_url_prefix}/api/asset/upload",
            headers={
                "Authorization": f"Bearer {self._auth_token}",
                "Content-Type": "application/json",
            },
            json={
                "ownerName": owner_name,
                "projectName": project_name,
                "assetPath": asset_path
            }
        )
        if not response.ok:
            return result.set_error(response.json().get("error"))

        result.asset_path = asset_path
        result.blob_path = response.json().get("blobPath")
        signed_url = response.json().get("signedUrl")

        try:
            if not signed_url:
                return result.set_error("Failed to get signed URL")

            headers = {
                "Content-Disposition": f"attachment; filename={os.path.basename(asset_path)}",
            }
            response = requests.put(signed_url, headers=headers, data=data)
            if not response.ok:
                return result.set_error(response.json().get("error"))
            else:
                return result.set_success()
        except Exception as e:
            return result.set_error(f"Unexpected error when uploading asset: {e}")
