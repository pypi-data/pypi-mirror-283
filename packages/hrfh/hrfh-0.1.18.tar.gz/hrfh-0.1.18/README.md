## Usage

```bash
pip install hrfh
```

```python
from hrfh.utils.parser import create_http_response_from_bytes
response = create_http_response_from_bytes(b"""HTTP/1.0 200 OK\r\nServer: nginx\r\nServer: apache\r\nETag: ea67ba7f802fb5c6cfa13a6b6d27adc6\r\n\r\n""")
print(response)
print(response.masked)
print(response.fuzzy_hash())
```

```python
>>> from hrfh.utils.parser import create_http_response_from_bytes
[nltk_data] Downloading package wordnet to /root/nltk_data...
[nltk_data] Downloading package words to /root/nltk_data...
[nltk_data]   Unzipping corpora/words.zip.
[nltk_data] Downloading package punkt to /root/nltk_data...
[nltk_data]   Unzipping tokenizers/punkt.zip.
>>> response = create_http_response_from_bytes(b"""HTTP/1.0 200 OK\r\nServer: nginx\r\nServer: apache\r\nETag: ea67ba7f802fb5c6cfa13a6b6d27adc6\r\n\r\n""")
>>> print(response)
<HTTPResponse 1.1.1.1:80 200 OK>
>>> print(response.masked)
HTTP/1.0 200 OK
ETag: [MASK]
Server: apache
Server: nginx
>>> print(response.fuzzy_hash())
ba15cc1f9ad3ef632d0ce7798f7fa44718f1e7fcc2c0f94c1a702f647b79923b
```

## Source Usage

1. Install requirements

```bash
sudo apt install python3-pip
```

```bash
pip install poetry
poetry install
poetry run python main.py
```

2. Prepare HTTP response data as json format in `data/${cdn}/${ip}.json` file

```bash
$ tree data/
data
├── akamai
│   ├── 104.103.147.116.json
│   └── 104.81.222.211.json
├── alibaba-cdn
└── wangsu
```

```bash
cat data/akamai/104.103.147.116.json
```

```json
{
  "ip": "104.103.147.116",
  "timestamp": 1717146116,
  "status_code": 400,
  "status_reason": "Bad Request",
  "headers": {
    "Server": "AkamaiGHost",
    "Mime-Version": "1.0",
    "Content-Type": "text/html",
    "Content-Length": "312",
    "Expires": "Fri, 31 May 2024 09:01:56 GMT",
    "Date": "Fri, 31 May 2024 09:01:56 GMT",
    "Connection": "close"
  },
  "body": "<HTML><HEAD>\n<TITLE>Invalid URL</TITLE>\n</HEAD><BODY>\n<H1>Invalid URL</H1>\nThe requested URL \"&#91;no&#32;URL&#93;\", is invalid.<p>\nReference&#32;&#35;9&#46;8be83217&#46;1717146116&#46;2661874a\n<P>https&#58;&#47;&#47;errors&#46;edgesuite&#46;net&#47;9&#46;8be83217&#46;1717146116&#46;2661874a</P>\n</BODY></HTML>\n"
}
```

3. Run the script to generate the hash 

```bash
poetry run python main.py
```

```
01c7da5c66ffab8b54a <HTTPResponse 45.64.21.148:80 403 Forbidden>
01c7da5c66ffab8b54a <HTTPResponse 103.151.139.204:80 403 Forbidden>
01c7da5c66ffab8b54a <HTTPResponse 199.91.74.213:80 403 Forbidden>
01c7da5c66ffab8b54a <HTTPResponse 156.59.207.6:80 403 Forbidden>
01c7da5c66ffab8b54a <HTTPResponse 23.90.149.102:80 403 Forbidden>
100c01467b6bb4c99e7 <HTTPResponse 58.57.102.41:80 403 Forbidden>
100c01467b6bb4c99e7 <HTTPResponse 60.188.66.41:80 403 Forbidden>
100c01467b6bb4c99e7 <HTTPResponse 117.68.34.41:80 403 Forbidden>
100c01467b6bb4c99e7 <HTTPResponse 124.225.184.41:80 403 Forbidden>
100c01467b6bb4c99e7 <HTTPResponse 58.42.14.41:80 403 Forbidden>
100c01467b6bb4c99e7 <HTTPResponse 101.206.106.41:80 403 Forbidden>
```

## Customize

### Load from another source

1. Implement your load which returns a [`HTTPResponse`](hrfh/models/__init__.py) object.
2. call `HTTPResponse.fuzzy_hash()` to get the hash of the http response.

## Python 3.7 Support

```python
$ docker run -i -t python:3.7 /bin/bash
root@aa0241a5a2f5:/# python --version
Python 3.7.12
root@aa0241a5a2f5:/# pip --version
pip 24.0 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)
root@aa0241a5a2f5:/# pip install --upgrade -q ipython hrfh==0.1.3
root@aa0241a5a2f5:/# ipython
Python 3.7.12 (default, Dec 21 2021, 11:25:13) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.34.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from hrfh.utils.parser import create_http_response_from_bytes
[nltk_data] Downloading package wordnet to /root/nltk_data...
[nltk_data] Downloading package words to /root/nltk_data...
[nltk_data]   Unzipping corpora/words.zip.
[nltk_data] Downloading package punkt to /root/nltk_data...
[nltk_data]   Unzipping tokenizers/punkt.zip.

In [2]: response = create_http_response_from_bytes(b"""HTTP/1.0 200 OK\r\nServer: nginx\r\nServer: apache\r\nETag: ea67ba7f802fb5c6cfa13a6b6d27adc6\r\n\r\n""")

In [3]: response.masked
Out[3]: 'HTTP/1.0 200 OK\nETag: [MASK]\nServer: apache\nServer: nginx'

In [4]: response.fuzzy_hash()
Out[4]: 'ba15cc1f9ad3ef632d0ce7798f7fa44718f1e7fcc2c0f94c1a702f647b79923b'
```