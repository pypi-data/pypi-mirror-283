from google.cloud import storage
import os

from zeta.usd.resolve import AssetFetcher
from zeta.utils.logging import zetaLogger

class AssetDownloader(object):
    _bucket_name = "gozeta-prod.appspot.com"
    _storage_client = storage.Client()
    _bucket = _storage_client.get_bucket(_bucket_name)

    @classmethod
    def download_asset(cls, asset_blobname: str, temp_path: str):
        asset_blob = cls._bucket.blob(asset_blobname)
        if not asset_blob.exists():
            zetaLogger.warning(f"asset '{asset_blobname}' does not exist")
            return ""

        asset_filename: str = os.path.join(temp_path, asset_blobname)
        asset_dirname: str = os.path.dirname(asset_filename)
        if not os.path.exists(asset_dirname):
            os.makedirs(asset_dirname)
        asset_blob.download_to_filename(asset_filename)

        return asset_filename


# Register the asset downloader callback
AssetFetcher.GetInstance().SetOnFetchCallback(AssetDownloader.download_asset)