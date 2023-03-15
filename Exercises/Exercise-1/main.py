import requests
import os
import logging
import zipfile
from pathlib import Path

download_uris = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip'
]

logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s", level=logging.DEBUG
)

log = logging.getLogger()


def create_dir(folderpath: Path) -> None:
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)

def check_urls(url: str) -> bool:
    r = requests.head(url)
    if r.status_code == 200:
        return True
    else:
        log.warning("URL: {url} doesn't exists")

def download_file(url: str, filepath: Path) -> None:
    response = requests.get(url)
    open(filepath, "wb").write(response.content)

def unzip_file(filepath: Path, newfilepath: Path):
    log.info(f"Unzipping file to {filepath}")
    try:
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(newfilepath)
    except Exception as e:
        print(f"Error: {e}")

def delete_file(filepath: Path) -> None:
    log.info(f"Deleting {filepath}")
    if os.path.exists(filepath):
        os.remove(filepath)

def main():
    #your code here
    Folderpath = Path("./downloads")

    #Create a directory downloads
    create_dir(folderpath=Folderpath)

    for url in download_uris:
        filepath = Folderpath/url.split("/")[-1]
        if check_urls(url):
            download_file(url=url, filepath=filepath)
            unzip_file(filepath=filepath, newfilepath=Folderpath)
            delete_file(filepath=filepath)
        else:
            log.warning(f"Couldn't download {url}. Skipping")

if __name__ == "__main__":
    main()