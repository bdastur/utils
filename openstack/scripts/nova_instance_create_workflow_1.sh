#!/bin/bash

###################################################################
# Workflow:
# nova instance creation. 
# Create instance --> create floating ip --> associate floating ip 
# to instance.
###################################################################

set -e

source ./setup_config.sh


# Get instance from nova list.
function get_nova_instance_from_list {
    local instance_name=$1
    nova_instance=`nova list | grep ${instance_name} | \
        awk -F"|" '{print $2 }'`
    if [ ! -z "$nova_instance" ]; then
        echo $nova_instance 
    fi
}

# Get glance id for specific image (name)
function get_glance_id_from_name {
    local glance_image=$1
    glance_id=`glance image-list | grep ${IMAGE_NAME} \
        | awk -F"|" '{print $2 }'| tr -d '[[:space:]]'`
    if [ ! -z "$glance_id" ]; then
        echo $glance_id
    fi
}

GLANCE_ID=`get_glance_id_from_name ${IMAGE_NAME}`
echo "GLANCE ID: ${GLANCE_ID}"

# Get Volume type id.
VOLUME_ID=`cinder --os-volume-api-version 1 type-list | grep ${VOLUME_TYPE} | awk -F"|" '{print $2}'| tr -d '[[:space:]]'`

echo "Volume id: ${VOLUME_ID}"

# Get flavor
FLAVOR_PRESENT=`nova flavor-list | grep ${FLAVOR_TYPE} | awk -F"|" '{print $3 }'`
echo "Flavor: ${FLAVOR_PRESENT}"

if [ -z "$FLAVOR_PRESENT" ]; then
    echo "Invalid flavor"
    exit 1 
fi

# Get neutron private and public net ids.
PRIVATE_NET_ID=`neutron net-list | grep $PRIVATE_NET | awk -F"|" '{print $2}'| tr -d '[[:space:]]'`
if [ -z $PRIVATE_NET_ID ]; then
    echo "Invalid private net"
    exit 1 
fi

PUBLIC_NET_ID=`neutron net-list | grep $PUBLIC_NET | awk -F"|" '{print $2}'| tr -d '[[:space:]]'`
if [ -z $PUBLIC_NET_ID ]; then
    echo "Invalid public net"
    exit 1
fi

echo "private: $PRIVATE_NET_ID, pub: $PUBLIC_NET_ID"


NOVA_INSTANCE=`get_nova_instance_from_list ${INSTANCE_NAME}`
echo "nova instance found: $NOVA_INSTANCE"

if [ -z "$NOVA_INSTANCE" ]; then
    nova boot --flavor ${FLAVOR_PRESENT} \
        --image ${IMAGE_NAME} \
        --nic net-id=${PRIVATE_NET_ID} ${INSTANCE_NAME}
fi
echo "instance creation done"

# Wait till it is active.
retry_cnt=5
pool_timer=5
while [ "$retry_cnt" -gt "0" ];
do
    echo "here 1 retry cnt: $retry_cnt"
    INSTANCE_STATE=`nova show ${INSTANCE_NAME} | grep ACTIVE`
    if [ ! -z "$INSTANCE_STATE" ]; then
        retry_cnt=0
        echo "Instance is Active"
    else
        echo "Instance is not active yet"
        retry_cnt=$(($retry_cnt-1))
    fi
    sleep $pool_timer
done

NOVA_INSTANCE=`get_nova_instance_from_list ${INSTANCE_NAME}`
echo "nova instance found: $NOVA_INSTANCE"
if [ -z "$NOVA_INSTANCE" ]; then
    echo "Nova instance not created."
    exit 1
fi

# Now get the port-id from the running instance.
# 1. First get the private assigned ip for the instance.
# 2. from the neutron port-list get the port-id associated with this ip.
PRIVATE_ASSIGNED_IP=`nova show brdtest_instance | grep ${PRIVATE_NET} | \
    awk -F"|" '{print $3}' | tr -d '[[:space:]]'`
if [ -z "$PRIVATE_ASSIGNED_IP" ]; then
    echo "Private assigned ip.. not present"
    exit 1
fi

PRIVATE_ASSIGNED_PORTID=`neutron port-list | grep ${PRIVATE_ASSIGNED_IP} | \
    awk -F"|" '{print $2}' | tr -d '[[:space:]]'`
if [ -z "$PRIVATE_ASSIGNED_PORTID" ]; then
    echo "Private assigned ip.. not present"
    exit 1
fi

neutron floatingip-create --port-id ${PRIVATE_ASSIGNED_PORTID} ${PUBLIC_NET_ID}

echo "DONE"


