#!/bin/bash

echo "Setup builder."

BUILDER_CONFIG_ROOT="/etc/builder"
BUILDER_CONFIG_DIR="${BUILDER_CONFIG_ROOT}/configs"
BUILDER_CONFIG_SCHEMA="${BUILDER_CONFIG_DIR}/schema.yaml"
BUILDER_THIRDPARTY_DIR="${BUILDER_CONFIG_ROOT}/thirdparty"

# Create builder config path.
if [[ ! -e ${BUILDER_CONFIG_ROOT} ]]; then
    echo "Builder config Root does not exist"
    mkdir -p ${BUILDER_CONFIG_DIR}
    mkdir -p ${BUILDER_THIRDPARTY_DIR}
fi

# Copy config files.
cp ./configs/builder.yaml ${BUILDER_CONFIG_ROOT}/builder.yaml
cp ./configs/dom_config.yaml ${BUILDER_CONFIG_DIR}/dom_config.yaml
cp ./configs/schema.yaml ${BUILDER_CONFIG_DIR}/schema.yaml
cp -R ./thirdparty ${BUILDER_THIRDPARTY_DIR}

