#!/bin/bash

silkit_uri="localhost:8501"
tap_name="silkit_tap"
tap_ip="192.168.7.2/16"

scriptDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

logDir=$scriptDir/logs # define a directory for .out files
mkdir -p $logDir # if it does not exist, create it

# cleanup trap for child processes
trap 'kill $(jobs -p); ip link set $tap_name down; ip link delete $tap_name; exit' EXIT SIGHUP;

# add lib path
export LD_LIBRARY_PATH=$scriptDir/lib:$LD_LIBRARY_PATH

# create TAP interface for SilKit
echo "Creating TAP interface..."
ip tuntap add dev $tap_name mode tap
ip addr add $tap_ip dev $tap_name
ip link set $tap_name up

sleep 1

# start SilKit components
echo "Starting sil-kit-registry..."
# ./silkit_tool/sil-kit-registry -c Silkit_can_set.silkit.yaml > $logDir/sil-kit-registry.out &
$scriptDir/bin/sil-kit-registry -u silkit://$silkit_uri &> $logDir/sil-kit-registry.out &

sleep 1

echo "Starting sil-kit-adaper-tap..."
$scriptDir/bin/sil-kit-adapter-tap --registry-uri silkit://$silkit_uri --tap-name $tap_name --log Debug &> $logDir/sil-kit-adapter_tap.out &

# start demo response, this can be removed if you do not need it
echo "Starting demo response..."
$scriptDir/demo/sil-kit-demo-ethernet-icmp-echo-device-tap --log Debug &> $logDir/sil-kit-demo_response.out &

wait
