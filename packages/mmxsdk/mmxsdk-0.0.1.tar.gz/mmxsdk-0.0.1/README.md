# mmxsdk

This is a Python SDK for MMX - https://github.com/madMAx43v3r/mmx-node a next
generation high performance blockchain.  There is currently no cloud services for this - 
you must have a local (or accessible) MMX node running.

All access requires the PASSWORD file generated during startup.  It's preferred you set this
in your environment as PASSWORD.  Don't enter it on the command line - set in your .bashrc or create a .env file.

PASSWORD isn't usable to perform any operations - it's like an OpenID secret used to generate a short lived token.

## Installation

Either download from Github directly and check into your source (preferred) or 

```base
pip install mmxsdk

```

## Using the SDK

Most operations require a session to be created.

```python
session = server.login(password=os.getenv("PASSWORD"))
`



NFT
mmx1af3nmx8zefduyqexz8z5v6qz2ks96znd89jxjk0jwtu9sqvvgmzqw7u6xt