import os

import requests
from rich.progress import wrap_file

from ..errors import ErrorPrinter


def __get_uploaded_bytes(upload_url):
    headers = {"Content-Range": "bytes */*"}
    response = requests.put(upload_url, headers=headers)
    if response.status_code != 308:
        raise Exception(f"Failed to retrieve upload status: {response.status_code} {response.text}")

    # Parse the Range header to get the last byte uploaded
    range_header = response.headers.get("Range")
    if range_header:
        last_byte = int(range_header.split("-")[1])
        return last_byte + 1
    return 0


def upload_signed_url(signed_url, source_file_name, content_type):
    """
    Upload file to file storage with signed url and resumable upload.
    Resumable upload will only work with the same URL and not if a new signed URL is requested with the
    same object id.
    :param signed_url:
    :param source_file_name:
    :return:
    """

    file_size = os.path.getsize(source_file_name)
    headers = {"x-goog-resumable": "start", "content-type": content_type}
    response = requests.post(signed_url, headers=headers)
    if response.status_code not in (200, 201, 308):
        ErrorPrinter.print_generic_error(f"Failed to upload file: {response.status_code} - {response.text}")
        exit(1)

    upload_url = response.headers["Location"]

    # Check how many bytes have already been uploaded
    uploaded_bytes = __get_uploaded_bytes(upload_url)

    # Upload the remaining file in chunks
    # Not sure what a good chunk size is or if we even should have resumable uploads here, probably not..
    chunk_size = 256 * 1024 * 10
    # Upload the file in chunks
    with open(source_file_name, "rb") as f:
        with wrap_file(f, os.stat(source_file_name).st_size, description=f"Uploading {source_file_name}...") as file:
            file.seek(uploaded_bytes)  # Seek to the position of the last uploaded byte
            for chunk_start in range(uploaded_bytes, file_size, chunk_size):
                chunk_end = min(chunk_start + chunk_size, file_size) - 1
                chunk = file.read(chunk_end - chunk_start + 1)
                headers = {"Content-Range": f"bytes {chunk_start}-{chunk_end}/{file_size}"}
                response = requests.put(upload_url, headers=headers, data=chunk)
                if response.status_code not in (200, 201, 308):
                    ErrorPrinter.print_generic_error(f"Failed to upload file: {response.status_code} - {response.text}")
                    exit(1)

    print(f"File {source_file_name} uploaded successfully.")
