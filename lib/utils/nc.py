import os

from nc_py_api import NextcloudApp

NEXTCLOUD_USER = os.getenv("NEXTCLOUD_USER")
NEXTCLOUD_URL = os.getenv("NEXTCLOUD_URL")

def get_nextcloud_app() -> NextcloudApp:
    """Get the NextcloudApp instance."""
    return NextcloudApp(
        nextcloud_url=NEXTCLOUD_URL,
        user=NEXTCLOUD_USER,
    )

def get_setings(nc: NextcloudApp, key: str, default=None):
    """Get settings value from the appconfig."""
    return nc.appconfig_ex.get_value(key, default)
