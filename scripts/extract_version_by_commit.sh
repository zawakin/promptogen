#!/bin/bash

set -eu

COMMIT_HASH=$1
PYPROJECT_PATH=$2

# extract version from file of specified commit
VERSION=$(git show $COMMIT_HASH:$PYPROJECT_PATH | grep version | awk '{print $NF}' | tr -d '"')

echo $VERSION
