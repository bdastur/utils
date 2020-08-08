#!/bin/bash

packer build -var-file variables.json ./templates/centos7.json
