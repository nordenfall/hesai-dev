#!/usr/bin/env bash
set -eo pipefail

source /opt/ros/jazzy/setup.bash
ros2 bag info $1 | grep Ima