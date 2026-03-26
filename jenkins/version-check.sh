#!/bin/bash

# Read current version
VERSION=$(cat version.txt)
echo "Current version: $VERSION"

# Check which components changed in the last commit
CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD)

ENGINE_CHANGED=false
CLI_CHANGED=false

if echo "$CHANGED_FILES" | grep -q "^modules/\|^seyoawe.linux\|^run.sh\|^configuration/"; then
    ENGINE_CHANGED=true
    echo "Engine changes detected"
fi

if echo "$CHANGED_FILES" | grep -q "^sawectl/"; then
    CLI_CHANGED=true
    echo "CLI changes detected"
fi

# Export flags for Jenkins to use
echo "ENGINE_CHANGED=$ENGINE_CHANGED" > build_flags.env
echo "CLI_CHANGED=$CLI_CHANGED" >> build_flags.env
echo "VERSION=$VERSION" >> build_flags.env

echo "Build flags written to build_flags.env"