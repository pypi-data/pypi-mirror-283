import requests
import zipfile
import os
from tqdm import tqdm
import site

def get_latest_pypi_package_url(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_version = data['info']['version']
        for file_info in data['releases'][latest_version]:
            if file_info['packagetype'] == 'bdist_wheel':
                return file_info['url']
    else:
        print(f"Failed to get package info: {response.status_code}")
        return None

def download_file(url, local_filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    with open(local_filename, 'wb') as file, tqdm(
        desc=local_filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)

def extract_wheel(file_path, extract_to='.'):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def get_pypi_package_code(package_name, download_dir='.'):
    print(f"Getting URL for the latest version of {package_name}...")
    url = get_latest_pypi_package_url(package_name)
    if url is None:
        print(f"Could not find a URL for {package_name}")
        return
    print(f"URL found: {url}")
    
    local_filename = os.path.join(download_dir, url.split('/')[-1])
    print(f"Downloading {url} to {local_filename}...")
    download_file(url, local_filename)
    
    print(f"Extracting {local_filename} to {download_dir}...")
    extract_wheel(local_filename, download_dir)
    
    print(f"Removing {local_filename}...")
    os.remove(local_filename)
    print(f"Finished downloading and extracting {package_name}")

def installjzai():
    package_name = 'jzai'
    download_dir = site.getsitepackages()
    download_dir = download_dir[1]
    get_pypi_package_code(package_name, download_dir)
