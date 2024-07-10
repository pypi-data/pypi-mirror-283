import ctypes
import os
import urllib.request

from sys        import platform
from platform   import machine


def __cffi__() -> str:
    if platform == 'darwin':
        file_ext = '-osx-arm64' if machine() == "arm64" else '-osx-x64'
    elif platform in ('win32', 'cygwin'):
        file_ext = '-win-x64.exe' if 8 == ctypes.sizeof(ctypes.c_voidp) else '-win-x86.exe'
    else:
        if machine() == "aarch64":
            file_ext = '-linux-arm64'
        elif "x86" in machine():
            file_ext = '-linux-arm'
        else:
            file_ext = '-linux-x64'

    root_dir = os.path.abspath(os.path.dirname(__file__))

    if not os.path.exists(f'{root_dir}/c/tlsnet{file_ext}'): # File not exists download first
        # Download the file from the URL and save it to the specified path
        try:
            f = f'{root_dir}/c/tlsnet{file_ext}'
            url = f'https://github.com/torstenprivate/httpso/raw/main/binaries/tlsnet{file_ext}'
            print(f"Initial download of binary file")
            with urllib.request.urlopen(url) as response:
                # Read the data from the URL
                data = response.read()

            # Write the data to a file
            with open(f'{root_dir}/c/tlsnet{file_ext}', 'wb') as file:
                file.write(data)
            print(f"Binary file successfully downloaded and saved to {f}")
        except Exception as e:
            print(f"Error downloading the binary: {e}")

    return f'{root_dir}/c/tlsnet{file_ext}'