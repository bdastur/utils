#!/bin/bash

###################################################################
# Volume operations:
# Create a volume if not exist, attach it to an instance. 
###################################################################

set -e

source ./osutils.sh


show_help () {
    echo "$0 - Cleanup Instance"
    echo "Options "
    echo "    -i : Instance name"
    echo "    -v : Volume name"
    echo "    -h : help"
}


# Parse command line
while getopts "d:i:hv:s:" Option
do
  case $Option in
    d) device_name=$OPTARG;;
    i) instance_name=$OPTARG;;
    h) show_help; exit 0;;
    s) size=$OPTARG;;
    v) volume=$OPTARG;;
    *) echo "Error: invalid option \"-$OPTARG\""; exit 1;;
    :) echo "Error: option \"-$OPTARG\" needs argument"; exit 1;;
  esac
done
echo "inst: $instance_name"

if [ -z "$instance_name" ]; then
    echo "-i <instance name> required"
    exit 1
fi

# Check if instance id present.
INSTANCE_ID=$(get_instance_id $instance_name)
if [ -z "$INSTANCE_ID" ]; then
    echo "Instance $instance_name, not found"
    exit 1
fi

# Check if volume and size are specified
if [ -z "$size" ]; then
    size="1"
fi

if [ -z "$volume" ]; then
    volume="testvolume"$(date +"%y%m%d%M%S")
fi

if [ -z "$device_name" ]; then
    device_name="/dev/vdb"
fi

echo "volume: $volume"

VOLUMES=`cinder --os-volume-api-version 1 list | \
    grep $volume | awk -F "|" '{print $2 }' | tr -d '[[:space:]]'`
if [ -z "$VOLUMES" ]; then
    # Create a new volume.
    echo "Create a new volume"
    cinder --os-volume-api-version 1 create --display-name $volume $size
fi

volume_id=`cinder --os-volume-api-version 1 list | \
    grep $volume | awk -F "|" '{print $2 }' | tr -d '[[:space:]]'`

nova volume-attach $instance_name $volume_id $device_name

echo "Done"


