import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import PIL.Image

s3_client = boto3.client('s3')

def resize_image(image_path, resized_path):
  with Image.open(image_path) as image:
      image.thumbnail(tuple(x / 2 for x in image.size))
      image.save(resized_path)
      
def resize_image2(image_path, resized_path):
  with Image.open(image_path) as image:
      image.thumbnail(tuple(x / 4 for x in image.size))
      image.save(resized_path)
      
def lambda_handler(event, context):
  for record in event['Records']:
    #recuperamos el bucket
      bucket = record['s3']['bucket']['name']
      key = unquote_plus(record['s3']['object']['key'])
      tmpkey = key.replace('/', '')
      #se baja el objeto
      download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
      #creamos un path para cada imagen que vamos a reducir
      upload_path2 = '/tmp/reducido-{}'.format(tmpkey)
      upload_path = '/tmp/minuatura-{}'.format(tmpkey)
      #bajamos el objeto que vamos a reducir
      s3_client.download_file(bucket, key, download_path)
      #cabiamos el tamnio de las fotos
      resize_image(download_path, upload_path)
      resize_image2(download_path, upload_path2)
      #subimos las fotos a sus bucket
      s3_client.upload_file(upload_path, 'size-o-reducido', key)
      s3_client.upload_file(upload_path2, 'size-o-miniatura', key)
      #   s3_client.upload_file(upload_path, '{}-reducido'.format(bucket), key)
      #s3_client.upload_file(upload_path2, '{}-miniatura'.format(bucket), key)