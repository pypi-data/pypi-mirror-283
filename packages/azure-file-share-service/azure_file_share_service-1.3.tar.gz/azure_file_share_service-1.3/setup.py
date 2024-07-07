from setuptools import setup, find_packages

setup(
    name="azure-file-share-service",
    version="1.3",
    packages=find_packages(),
    install_requires=[
        "azure-identity",
        "azure-storage-file-share",
        "azure-core",
    ],
    entry_points={
        "console_scripts": [
            "azure_file_share_service=azure_file_share_service.main:main",
        ]
    },
    license='MIT',
    description='Helper to download/upload files to azure file share',
    url='https://github.com/DelphianCalamity/azure_file_share_service',
    download_url="https://github.com/DelphianCalamity/azure_file_share_service/archive/refs/tags/v0.tar.gz",
)
