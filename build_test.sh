#!/bin/bash

export PATH=\
/opt/buildout.python/bin:\
$PATH:

if [[ "$1" = "plone-4.3" ]]
then
    config=buildout-plone-4.3.cfg
fi

if [[ "$1" = "plone-5.0" ]]
then
    config=buildout-plone-5.0.cfg
fi

export WEBDAV_URL=http://docker.zopyx.com:22081/exist/webdav/db

virtualenv-2.7 .
bin/pip install -U setuptools==7.0  --version=2.2.5
bin/python bootstrap.py -c $config
bin/buildout -c $config
bin/test -s xmldirector
#bin/coverage run bin/test
