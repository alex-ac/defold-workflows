# defold-workflows

Github actios workflow for building games on defold.

Builds and uploads defold project for all platforms:

 - Linux x86\_64;
 - Windows x86;
 - Windows x86\_64;
 - MacOS x86\_64;
 - Android armv7,arm64;
 - iOS arm64;
 - WebAssembl;

Usage:
```
name: CI
on:
  push:
  - master
  pull_request:
  - master
jobs:
  defold:
    uses: alex-ac/defold-workflows/.github/workflows/build.yaml@v1.0.0
```

Inputs:

 * `project_path` - path to the defold project (if not in the repo root).
 * `defold_version` - sha1 of the defold engine version or the channel
   (`stable`, `beta` or `alpha`).

Known issues:

 * No way to setup signing of Android/iOS app. Would fix in future version.
