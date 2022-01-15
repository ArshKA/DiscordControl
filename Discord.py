import brotli
import json
import time
from fake_headers import Headers
import requests

header_gen = Headers(headers=True)

ID = #enter channel ID here
authorization = #enter authorization here

class Discord:
  def __init__(self, channel_id, authorization):
    self.channel = channel_id

    self.message_header = header_gen.generate()
    self.message_header['authorization'] = authorization
    self.message_header['Referer'] = 'https://discord.com'
    self.message_header['content-type'] = 'application/json'

    self.read_header = header_gen.generate()
    self.read_header['authorization'] = authorization
    self.read_header['accept-encoding'] = 'gzip;q=0, deflate, br'
    self.read_header['encoding'] = 'json'
    self.read_header['sec-fetch-dest'] = 'empty'
    self.read_header['sec-fetch-mode'] = 'cors'
    self.read_header['sec-fetch-site'] = 'same-origin'
    self.read_header['content-type'] = 'application/json'

  def read_response(self, text):
    data = brotli.decompress(text)
    data = json.loads(data)
    return data

  def check_response(self, response):
    if response.status_code < 200 and response.status_code > 299:
      print(response, response.headers)
      return False
    return True

  def typing(self):
    response = requests.post('https://discord.com/api/v9/channels/{}/typing'.format(self.channel), headers=self.message_header)
    time.sleep(1)
    return self.check_response(response)

  def send_message(self, text):
    self.typing()
    payload = json.dumps({"content" : text})
    response = requests.post('https://discord.com/api/v8/channels/{}/messages'.format(self.channel), data=payload, headers=self.message_header)
    time.sleep(3)
    return self.check_response(response)

  
  def read_messages(self, limit):
    response = requests.get('https://discord.com/api/v9/channels/{}/messages?limit={}'.format(self.channel, limit), headers=self.read_header)
    time.sleep(2)
    return self.read_response(response.content)

channel = Discord(ID, authorization)
