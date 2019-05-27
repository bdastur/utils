#!/bin/bash

echo "Setup builder."

BUILDER_CONFIG_ROOT="/etc/builder"
BUILDER_CONFIG_SCHEMA="/etc/builder/config/schema.yaml"

# Create builder config path.
if [[ ! -e ${BUILDER_CONFIG_ROOT} ]]; then
    echo "Builder config Root does not exist"
    mkdir -p /etc/builder
    mkdir -p /etc/builder/config
fi

# Copy config files.

