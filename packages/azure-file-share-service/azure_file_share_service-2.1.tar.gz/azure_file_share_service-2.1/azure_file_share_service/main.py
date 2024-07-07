import os
import logging
from typing import Set
import argparse

from azure.storage.fileshare import ShareClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError


_LOG = logging.getLogger(__name__)


class AzureFileShareService:
    """
    Helper class for interacting with Azure File Share
    """

    _SHARE_URL = "https://{account_name}.file.core.windows.net/{fs_name}"

    def __init__(self, config: dict):
        self.config = config

        assert "tenantId" in self.config
        assert "storageAccountName" in self.config
        assert "storageFileShareName" in self.config
        assert "managedIdentityClientId" in self.config

        os.environ["AZURE_CLIENT_ID"] = self.config["managedIdentityClientId"]
        os.environ["AZURE_TENANT_ID"] = self.config["tenantId"]

        args = {
            "exclude_workload_identity_credential": True,
            "exclude_developer_cli_credential": True,
            "exclude_cli_credential": True,
            "exclude_powershell_credential": True,
            "exclude_shared_token_cache_credential": True,
            "exclude_interactive_browser_credential": True,
            "exclude_visual_studio_code_credential": True,
            "exclude_environment_credential": True,
        }
        self._share_client = ShareClient.from_share_url(
            AzureFileShareService._SHARE_URL.format(
                account_name=self.config["storageAccountName"],
                fs_name=self.config["storageFileShareName"],
            ),
            credential=DefaultAzureCredential(**args),
            token_intent="backup",
        )

    def download(
        self, remote_path: str, local_path: str, recursive: bool = True
    ) -> None:
        _LOG.info(
            "Download from File Share %s recursively: %s -> %s",
            "" if recursive else "non",
            remote_path,
            local_path,
        )

        dir_client = self._share_client.get_directory_client(remote_path)
        if dir_client.exists():
            os.makedirs(local_path, exist_ok=True)
            for content in dir_client.list_directories_and_files():
                name = content["name"]
                local_target = f"{local_path}/{name}"
                remote_target = f"{remote_path}/{name}"
                if recursive or not content["is_directory"]:
                    self.download(remote_target, local_target, recursive)
        else:  # Must be a file
            # Ensure parent folders exist
            folder, _ = os.path.split(local_path)
            os.makedirs(folder, exist_ok=True)
            file_client = self._share_client.get_file_client(remote_path)
            try:
                data = file_client.download_file()
                with open(local_path, "wb") as output_file:
                    _LOG.debug("Download file: %s -> %s", remote_path, local_path)
                    data.readinto(output_file)  # type: ignore[no-untyped-call]
            except ResourceNotFoundError as ex:
                # Translate into non-Azure exception:
                raise FileNotFoundError(f"Cannot download: {remote_path}") from ex

    def upload(self, local_path: str, remote_path: str, recursive: bool = True) -> None:
        _LOG.info(
            "Upload to File Share %s recursively: %s -> %s",
            "" if recursive else "non",
            local_path,
            remote_path,
        )
        self._upload(local_path, remote_path, recursive, set())

    def _upload(
        self, local_path: str, remote_path: str, recursive: bool, seen: Set[str]
    ) -> None:
        """
        Upload contents from a local path to an Azure file share.
        This method is called from `.upload()` above. We need it to avoid exposing
        the `seen` parameter and to make `.upload()` match the base class' virtual
        method.

        Parameters
        ----------
        local_path : str
            Path to the local directory to upload contents from, either a file or directory.
        remote_path : str
            Path in the remote file share to store the uploaded content to.
        recursive : bool
            If False, ignore the subdirectories;
            if True (the default), upload the entire directory tree.
        seen: Set[str]
            Helper set for keeping track of visited directories to break circular paths.
        """
        local_path = os.path.abspath(local_path)
        if local_path in seen:
            _LOG.warning("Loop in directories, skipping '%s'", local_path)
            return
        seen.add(local_path)

        if os.path.isdir(local_path):
            self._remote_makedirs(remote_path)
            for entry in os.scandir(local_path):
                name = entry.name
                local_target = f"{local_path}/{name}"
                remote_target = f"{remote_path}/{name}"
                if recursive or not entry.is_dir():
                    self._upload(local_target, remote_target, recursive, seen)
        else:
            # Ensure parent folders exist
            folder, _ = os.path.split(remote_path)
            self._remote_makedirs(folder)
            file_client = self._share_client.get_file_client(remote_path)
            with open(local_path, "rb") as file_data:
                _LOG.debug("Upload file: %s -> %s", local_path, remote_path)
                file_client.upload_file(file_data)

    def _remote_makedirs(self, remote_path: str) -> None:
        """
        Create remote directories for the entire path.
        Succeeds even some or all directories along the path already exist.

        Parameters
        ----------
        remote_path : str
            Path in the remote file share to create.
        """
        path = ""
        for folder in remote_path.replace("\\", "/").split("/"):
            if not folder:
                continue
            path += folder + "/"
            dir_client = self._share_client.get_directory_client(path)
            if not dir_client.exists():
                dir_client.create_directory()

    def list_files(self, remote_path: str):
        dir_client = self._share_client.get_directory_client(remote_path)
        for content in dir_client.list_directories_and_files():
            print(content)
            # _LOG.info(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--function", type=str, help="", required=True)
    parser.add_argument("--local_path", type=str, help="", default=None)
    parser.add_argument("--remote_path", type=str, help="", required=True)
    parser.add_argument("--recursive", type=bool, help="", default=True)
    args = parser.parse_args()

    storage_account_name = os.getenv('storageAccountName')
    storage_file_share_name = os.getenv('storageFileShareName')
    managed_identity_client_id = os.getenv('managedIdentityClientId')
    tenant_id = os.getenv('tenantId')

    config = {
        "storageAccountName": str(storage_account_name),
        "storageFileShareName": str(storage_file_share_name),
        "managedIdentityClientId": str(managed_identity_client_id),
        "tenantId": str(tenant_id),
    }
    azure_file_share_service = AzureFileShareService(config)
    if args.function == "list_files":
        azure_file_share_service.list_files(remote_path=args.remote_path)
    elif args.function == "upload":
        azure_file_share_service.upload(
            local_path=args.local_path,
            remote_path=args.remote_path,
            recursive=args.recursive,
        )
    elif args.function == "download":
        azure_file_share_service.download(
            remote_path=args.remote_path,
            local_path=args.local_path,
            recursive=args.recursive,
        )
    else:
        raise ValueError(f"Function {args.function} not supported")


if __name__ == "__main__":
    main()
