# tiny-ci-server
A tiny ci server in python

## How to use

You need to set two environment variables first
`export SECRET=abcdefghij`
`export REPO=gdury/tiny-ci-server`
`python server.py`

It will start a server on port 4532 to listen to POST request from Github with a hashed signature

#test
