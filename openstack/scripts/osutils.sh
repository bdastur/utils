#!/bin/bash

###########################################################
# Common Functions for OpenStack CLI operations.
###########################################################


# Get instance from nova list.                                                                            
function get_instance_id {
    local instance_name=$1
    nova_instance=`nova list | grep ${instance_name} | \
        awk -F"|" '{print $2 }'`
    if [ ! -z "$nova_instance" ]; then
        echo $nova_instance 
    fi
}

# Get volumes attached to an instance.
function get_instance_volumes {
    local instance_id=$1
    volume_list=(`cinder --os-volume-api-version 1 list | \
        grep ${instance_id} | \
        awk -F "|" '{print $2 }' | tr -d '[[:space:]]'`)
    if [ ! -z "$volume_list" ]; then
        echo $volume_list
    fi
}

# Detach given volumes for the specific instance.
function detach_volumes {
    local instance_id=$1
    local volumes=($2)
    for volume in "${volumes[@]}"
    do
        echo "Detaching volume $volume from ${instance_id}"
        nova volume-detach $instance_id $volume
    done
}




