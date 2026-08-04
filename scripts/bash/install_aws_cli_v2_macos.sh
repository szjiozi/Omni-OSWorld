#!/usr/bin/env bash

set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This installer is only for macOS." >&2
  exit 1
fi

if [[ -z "${CONDA_PREFIX:-}" || "${CONDA_DEFAULT_ENV:-}" != "osworld-aws-dev" ]]; then
  echo "Activate the osworld-aws-dev Conda environment first." >&2
  exit 1
fi

installer_dir="$(mktemp -d)"
trap 'rm -rf "${installer_dir}"' EXIT

package_path="${installer_dir}/AWSCLIV2.pkg"
choices_path="${installer_dir}/choices.xml"

curl --fail --location \
  "https://awscli.amazonaws.com/AWSCLIV2.pkg" \
  --output "${package_path}"

printf '%s\n' \
  '<?xml version="1.0" encoding="UTF-8"?>' \
  '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">' \
  '<plist version="1.0">' \
  '  <array>' \
  '    <dict>' \
  '      <key>choiceAttribute</key>' \
  '      <string>customLocation</string>' \
  '      <key>attributeSetting</key>' \
  "      <string>${CONDA_PREFIX}</string>" \
  '      <key>choiceIdentifier</key>' \
  '      <string>default</string>' \
  '    </dict>' \
  '  </array>' \
  '</plist>' >"${choices_path}"

installer \
  -pkg "${package_path}" \
  -target CurrentUserHomeDirectory \
  -applyChoiceChangesXML "${choices_path}"

"${CONDA_PREFIX}/bin/python" -m pip uninstall -y awscli >/dev/null 2>&1 || true
ln -sfn ../aws-cli/aws "${CONDA_PREFIX}/bin/aws"
ln -sfn ../aws-cli/aws_completer "${CONDA_PREFIX}/bin/aws_completer"

aws_version="$(aws --version 2>&1)"
if [[ "${aws_version}" != aws-cli/2.* ]]; then
  echo "AWS CLI v2 verification failed: ${aws_version}" >&2
  exit 1
fi

echo "Installed ${aws_version}"
