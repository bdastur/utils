#!/bin/bash

###################################################################
# Cleanup instance and all associated resources (volumes, floatingip) 
###################################################################

set -e

# Get instance from nova list.
function get_instance_id {
    local instance_name=$1
    nova_instance=`nova list | grep ${instance_name} | \
        awk -F"|" '{print $2 }'`
    if [ ! -z "$nova_instance" ]; then
        echo $nova_instance 
    fi
}

# Get floating-ip associated to Instance.
function get_instance_floatingip {
    local instance_id=$1
    floating_ip_id=`nova floating-ip-list | grep ${instance_id} | \
        awk -F"|" '{print $2 }' | tr -d '[[:space:]]'`
    echo "$floating_ip_id"
}

# Get attached volumes.
function get_instance_volumes {
    local instance_id=$1
    volume_list=(`cinder --os-volume-api-version 1 list | \
        grep ${instance_id} | \
        awk -F "|" '{print $2 }' | tr -d '[[:space:]]'`)
    if [ ! -z "$volume_list" ]; then
        echo $volume_list
    fi
}

function detach_volumes {
    local instance_id=$1
    local volumes=($2)
    for volume in "${volumes[@]}"
    do
        echo "Detaching volume $volume from ${instance_id}"
        nova volume-detach $instance_id $volume
    done
}

function disassociate_floatingip {
    local floatingip_id=$1
    if [ -z "$floatingip_id" ]; then
        echo "No floating ip specified... exit"
    else
        neutron floatingip-disassociate $floatingip_id
    fi
}

function delete_instance {
    local instance_id=$1
    if [ -z "$instance_id" ]; then
        echo "No instance with id: $instance_id found"
    else
        nova delete $instance_id
    fi
}

function delete_floatingip {
    local floatingip_id=$1
    if [ -z "$floatingip_id" ]; then
        echo "No floatingip provided"
    else
        neutron floatingip-delete $floatingip_id
    fi
}

function delete_volumes {
local volumes=($1)
    if [ -z "$volumes" ]; then
        echo "No volumeid provided"
    else
        for volume in "${volumes[@]}"
        do
            echo "Deleting volume $volume"
            cinder --os-volume-api-version 1 delete $volume
        done
    fi
}

show_help () {
    echo "$0 - Cleanup Instance"
    echo "Options "
    echo "    -i : Instance name"
    echo "    -h : help"
}

echo "Invocation command line: [$*]"

# Parse command line
while getopts "i:hv" Option
do
  case $Option in
    i) instance_name=$OPTARG;;
    h) show_help; exit 0;;
    v) verbose=1;;
    *) echo "Error: invalid option \"-$OPTARG\""; exit 1;;
    :) echo "Error: option \"-$OPTARG\" needs argument"; exit 1;;
  esac
done
echo "inst: $instance_name"

if [ -z "$instance_name" ]; then
    echo "-i <instance name> required"
    exit 1
fi

INSTANCE_ID=$(get_instance_id $instance_name)
echo "INSTANCEID: ${INSTANCE_ID}"

FLOATINGIP=$(get_instance_floatingip $INSTANCE_ID)
echo "FLOATINGIP: $FLOATINGIP"

VOLUMES=$(get_instance_volumes $INSTANCE_ID)
for volume in "${VOLUMES[@]}"
do
    echo "volume: $volume"
done

detach_volumes ${INSTANCE_ID} ${VOLUMES}
disassociate_floatingip ${FLOATINGIP}
delete_instance ${INSTANCE_ID}
delete_floatingip ${FLOATINGIP}
delete_volumes ${VOLUMES}

echo "Done"


