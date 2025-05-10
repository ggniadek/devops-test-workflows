#!/bin/bash
pip install --platform manylinux2014_x86_64 --target=python --implementation cp --python-version 3.11 --only-binary=:all: --upgrade icoscp==0.2.2 icoscp_core==0.3.9 matplotlib python-slugify || exit
zip -r python.zip python || rm -rf python