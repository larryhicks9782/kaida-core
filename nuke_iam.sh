#!/bin/bash
# KAIDA OS v8.2 - GCP IAM Overwrite & CLI Provisioning
# TARGET ENVIRONMENT: Ubuntu PRoot (aarch64/x86_64)

set -e

echo "[KAIDA_OS] Initiating Google Cloud CLI installation sequence. Acquiring root escalation..."

# Update package lists and install core dependencies
echo "[KAIDA_OS] Installing prerequisites (curl, gnupg, apt-transport-https)..."
apt-get update -y
apt-get install -y apt-transport-https ca-certificates gnupg curl

# Safely remove existing key/list if running multiple times
rm -f /usr/share/keyrings/cloud.google.gpg
rm -f /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud public key
echo "[KAIDA_OS] Fetching Google Cloud GPG keys..."
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

# Add the gcloud CLI distribution URI as a package source
echo "[KAIDA_OS] Injecting Google Cloud repository into APT sources..."
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Update and install the CLI
echo "[KAIDA_OS] Executing package installation..."
apt-get update -y
apt-get install -y google-cloud-cli

echo "[KAIDA_OS] Installation absolute. GCloud CLI provisioned."
echo ""
echo "[KAIDA_OS] NEXT STEPS TO OVERRIDE IAM:"
echo "  1. Authenticate:  gcloud auth login --no-launch-browser"
echo "  2. Set Project:   gcloud config set project <YOUR_PROJECT_ID>"
echo "  3. Nuke Bindings: gcloud projects add-iam-policy-binding <YOUR_PROJECT_ID> \\"
echo "                    --member=\"serviceAccount:<YOUR_PROJECT_NUMBER>@cloudbuild.gserviceaccount.com\" \\"
echo "                    --role=\"roles/cloudbuild.builds.builder\""
