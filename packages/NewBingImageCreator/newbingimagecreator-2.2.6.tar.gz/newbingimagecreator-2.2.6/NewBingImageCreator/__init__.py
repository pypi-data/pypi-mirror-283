import datetime
import json
import httpx
import time


class ImageCreator:
    def __init__(self) -> None:
        self.requests = httpx.Client()
        self.scope = None
        self.access_token = None
        self.vrefresh_token = None
        self.expires_in = None
        self.ms_token = None
        self.copilot_cokies = None
        self.login_url = "https://login.live.com/oauth20_authorize.srf?response_type=code&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf&scope=api%3A%2F%2F11278b67-0ad9-4a03-8ae7-e5070399d618%2FSwiftKeyConnect%20offline_access%20openid&client_id=ce80f643-ae76-472f-b4d1-755080f1f0e5&state=1g24kbm744cvo9f6t6cmp62dgu"

    def login(self, code):
        url = "https://login.live.com/oauth20_token.srf"

        payload = {
            "code": code,
            "client_id": "ce80f643-ae76-472f-b4d1-755080f1f0e5",
            "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
            "grant_type": "authorization_code",
        }

        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 14; ONEPLUS A5010 Build/AP1A.240505.005)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = self.requests.post(url, data=payload, headers=headers)

        r = response.json()
        self.scope = r["scope"]
        self.access_token = r["access_token"]
        self.vrefresh_token = r["refresh_token"]
        self.expires_in = datetime.datetime.now() + datetime.timedelta(
            seconds=r["expires_in"]
        )

    def check_and_refresh_token(self):
        if datetime.datetime.now() >= self.expires_in:
            self.refresh_token()

    def get_ms_token(self):
        self.check_and_refresh_token()

        url = "https://login.live.com/oauth20_token.srf"

        payload = {
            "client_id": "ce80f643-ae76-472f-b4d1-755080f1f0e5",
            "scope": "service::bing.com::MBI_SSL",
            "redirect_uri": "com.touchtype.swiftkey://swiftkey.com/auth/microsoft/account",
            "refresh_token": self.vrefresh_token,
            "grant_type": "refresh_token",
        }

        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 14; ONEPLUS A5010 Build/AP1A.240505.005)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = self.requests.post(url, data=payload, headers=headers)
        r = response.json()
        self.ms_token = r["access_token"]

    def refresh_token(self):
        url = "https://login.live.com/oauth20_token.srf"

        payload = {
            "client_id": "ce80f643-ae76-472f-b4d1-755080f1f0e5",
            "scope": self.scope,
            "redirect_uri": "com.touchtype.swiftkey://swiftkey.com/auth/microsoft/account",
            "refresh_token": self.vrefresh_token,
            "grant_type": "refresh_token",
        }

        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 14; ONEPLUS A5010 Build/AP1A.240505.005)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = self.requests.post(url, data=payload, headers=headers, timeout=60)

        r = response.json()
        self.access_token = r["access_token"]
        self.expires_in = datetime.datetime.now() + datetime.timedelta(
            seconds=r["expires_in"]
        )

    def get_ms_cokies(self):
        if not self.ms_token:
            self.get_ms_token()
        self.check_and_refresh_token()

        url = "https://ssl.bing.com/fd/auth/signin"

        params = {
            "action": "token",
            "provider": "windows_live_id",
            "save_token": "0",
            "token": self.ms_token,
        }

        headers = {"User-Agent": "okhttp/4.11.0", "Accept-Encoding": "gzip"}

        response = self.requests.get(url, params=params, headers=headers)

        cookies = response.cookies
        formatted_cookies = "; ".join(
            [f"{cookie}={cookies[cookie]}" for cookie in cookies]
        )

        self.copilot_cokies = formatted_cookies

    def tone_rewrite(self, query):
        if not self.copilot_cokies:
            self.get_ms_cokies()
        self.check_and_refresh_token()

        url = "https://www.bing.com/api/swiftkey/v1/toneRewrite/text"

        payload = json.dumps({"query": query, "enableHiddenTones": True})

        headers = {
            "User-Agent": "okhttp/4.11.0",
            "Accept-Encoding": "gzip",
            "authorization": f"Bearer {self.access_token}",
            "x-swiftkey-source": "swiftkey-android",
            "content-type": "application/json; charset=utf-8",
            "Cookie": self.copilot_cokies,
        }

        response = self.requests.post(url, data=payload, headers=headers, timeout=60)
        r = response.json()

        if "error" in r:
            return dict(suceess=False, error=r["error"])
        else:
            return dict(
                success=True, query=r["query"], tones=r["instructionsToRewrite"]
            )

    def text_improve(self, query):
        if not self.copilot_cokies:
            self.get_ms_cokies()
        self.check_and_refresh_token()

        url = "https://www.bing.com/api/swiftkey/v1/sydney/improve"

        payload = json.dumps({"query": query})

        headers = {
            "User-Agent": "okhttp/4.11.0",
            "Accept-Encoding": "gzip",
            "authorization": f"Bearer {self.access_token}",
            "x-swiftkey-source": "swiftkey-android",
            "content-type": "application/json; charset=utf-8",
            "Cookie": self.copilot_cokies,
        }

        response = self.requests.post(url, data=payload, headers=headers, timeout=60)
        r = response.json()

        if "error" in r:
            return dict(suceess=False, error=r["error"])
        else:
            return dict(success=True, query=r["query"], improved=r["improvedText"])

    def gen_image(self, query, locale="EN", removeBackground=False) -> list:
        if not self.copilot_cokies:
            self.get_ms_cokies()
        self.check_and_refresh_token()

        url = "https://www.bing.com/api/swiftkey/v1/image-creator/"

        payload = json.dumps(
            {
                "type": "com.microsoft.bingimagecreatornative.data.network.models.BingImageCreatorCreateRequest",
                "Query": query,
                "Locale": locale,
            }
        )

        headers = {
            "User-Agent": "okhttp/4.11.0",
            "Accept-Encoding": "gzip",
            "authorization": f"Bearer {self.access_token}",
            "x-swiftkey-source": "swiftkey-android",
            "content-type": "application/json; charset=utf-8",
            "Cookie": self.copilot_cokies,
        }

        response = self.requests.post(
            f"{url}create", data=payload, headers=headers
        )
        r = response.json()
        
        if "error" in r:
            return dict(suceess=False, error=r["error"])

        payload = json.dumps(
            {
                "type": "com.microsoft.bingimagecreatornative.data.network.models.BingImageCreatorRetrieveRequest",
                "RetrieveId": r["createdImagesRetrieveId"],
                "Query": r["query"],
                "RemoveBackground": removeBackground,
                "Width": None,
            }
        )

        images = []

        while not images:
            response = self.requests.post(
                f"{url}retrieve", data=payload, headers=headers, timeout=60
            )
            if "images" in response.json():
                images = response.json()["images"]
            time.sleep(1)

        return dict(success=True, images=images)

    def gen_sticker(self, query, locale="EN", removeBackground=True) -> list:
        if not self.copilot_cokies:
            self.get_ms_cokies()
        self.check_and_refresh_token()

        url = "https://www.bing.com/api/swiftkey/v1/gen-sticker/"

        payload = json.dumps(
            {
                "type": "com.microsoft.bingimagecreatornative.data.network.models.BingImageCreatorCreateRequest",
                "Query": query,
                "Locale": locale,
            }
        )

        headers = {
            "User-Agent": "okhttp/4.11.0",
            "Accept-Encoding": "gzip",
            "authorization": f"Bearer {self.access_token}",
            "x-swiftkey-source": "swiftkey-android",
            "content-type": "application/json; charset=utf-8",
            "Cookie": self.copilot_cokies,
        }

        response = self.requests.post(
            f"{url}create", data=payload, headers=headers
        )
        r = response.json()

        if "error" in r:
            return dict(suceess=False, error=r["error"])

        payload = json.dumps(
            {
                "type": "com.microsoft.bingimagecreatornative.data.network.models.BingImageCreatorRetrieveRequest",
                "RetrieveId": r["createdImagesRetrieveId"],
                "Query": r["query"],
                "RemoveBackground": removeBackground,
                "Width": None,
            }
        )

        images = []

        while not images:
            response = self.requests.post(
                f"{url}retrieve", data=payload, headers=headers, timeout=60
            )
            if "images" in response.json():
                images = response.json()["images"]
            time.sleep(1)

        return dict(success=True, images=images)

    def __str__(self) -> str:
        return f"scope: {self.scope}\naccess_token: {self.access_token}\nvrefresh_token: {self.vrefresh_token}\nexpires_in: {self.expires_in}\nms_token: {self.ms_token}"
