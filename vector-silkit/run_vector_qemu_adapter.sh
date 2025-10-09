#!/bin/bash

silkit_uri="localhost:8501"
network_name="qemu_demo"
socket_port="12345"

scriptDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

logDir=$scriptDir/logs # define a directory for .out files
mkdir -p $logDir # if it does not exist, create it

# cleanup trap for child processes
trap 'kill $(jobs -p); exit' EXIT SIGHUP;

# add lib path
export LD_LIBRARY_PATH=$scriptDir/lib:$LD_LIBRARY_PATH

# start SilKit components
echo "Starting sil-kit-registry..."
# ./silkit_tool/sil-kit-registry -c Silkit_can_set.silkit.yaml > $logDir/sil-kit-registry.out &
$scriptDir/bin/sil-kit-registry -u silkit://$silkit_uri &> $logDir/sil-kit-registry.out &

sleep 1

echo "Starting sil-kit-adaper-qemu..."
$scriptDir/bin/sil-kit-adapter-qemu --socket-to-ethernet localhost:$socket_port,network=$network_name --registry-uri silkit://$silkit_uri --log Debug &> $logDir/sil-kit-adapter_qemu.out &

# start demo response, this can be removed if you do not need it
echo "Starting demo response..."
$scriptDir/demo/sil-kit-demo-ethernet-icmp-echo-device-qemu --log Debug &> $logDir/sil-kit-demo_response.out &

wait
