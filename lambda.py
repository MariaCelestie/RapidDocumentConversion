import os
from io import BytesIO
import tarfile
import boto3
import subprocess
import brotli

libre_office_install_dir = '/tmp/instdir'

def load_libre_office():
    if os.path.exists(libre_office_install_dir) and os.path.isdir(libre_office_install_dir):
        print('We have a cached copy of LibreOffice, skipping extraction')
    else:
        print('No cached copy of LibreOffice exists, extracting tar stream from Brotli file.')
        buffer = BytesIO()
        with open('/opt/lo.tar.br', 'rb') as brotli_file:
            decompressor = brotli.Decompressor()
            while True:
                chunk = brotli_file.read(1024)
                buffer.write(decompressor.decompress(chunk))
                if len(chunk) < 1024:
                    break
            buffer.seek(0)

        print('Extracting tar stream to /tmp for caching.')
        with tarfile.open(fileobj=buffer) as tar:
            tar.extractall('/tmp')
        print('Done caching LibreOffice!')

    return f'{libre_office_install_dir}/program/soffice.bin'


def download_from_s3(bucket, key, download_path):
    s3 = boto3.client("s3")
    s3.download_file(bucket, key, download_path)


def upload_to_s3(file_path, bucket, key):
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket, key)


def convert_word_to_pdf(executable_path, word_file_path, output_dir):
    conv_cmd = f"{soffice_path} --headless --norestore --invisible --nodefault --nofirststartwizard --nolockcheck --nologo --convert-to pdf:writer_pdf_Export --outdir {output_dir} {word_file_path}"
    response = subprocess.run(conv_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if response.returncode != 0:
        response = subprocess.run(conv_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response.returncode != 0:
            return False
    return True


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['rapiddocuments3']['name']
    output_bucket = 'converteddocument'
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
# bucket = event["document_bucket"]
# key = event["document_key"]
    key_prefix, base_name = os.path.split(key)
    download_path = f"/tmp/{base_name}"
    output_dir = "/tmp"

    download_from_s3(bucket, key, download_path)

    soffice_path = load_libre_office()

    is_converted = convert_word_to_pdf(soffice_path, download_path, output_dir)
    if is_converted:
        file_name, _ = os.path.splitext(base_name)
        upload_to_s3(f"{output_dir}/{file_name}.pdf", output_bucket, f"{key_prefix}/{file_name}.pdf")
        return {"response": "file converted to PDF and available at same S3 location of input key"}
    else:
        return {"response": "cannot convert this document to PDF"}