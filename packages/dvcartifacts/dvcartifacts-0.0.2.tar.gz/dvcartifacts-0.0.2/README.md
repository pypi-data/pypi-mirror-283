## Getting artifacts from monorepo projects without cloning the entire monorepo

`dvcartifacts` is a Python CLI tool which relies on `gitPython` and SSH to authenticate with a remote Git repository.

It uses sparse checkout without downloading anything outside of the specified project directory to speed up the cloning (cloning the project is required for getting the URL of the versioned artifact).

### Important notes/limitations

Artifacts are assumed to be created in specific project subdirectories in a monorepo with the following structure, i.e. with each DVC project initialized in a separate subdirectory.

```
monorepo
    ├── project_1
    │   ├── .dvc
    │   │   ├── config
    │   │   └── .gitignore
    │   ├── .dvcignore
    │   ├── dvc.lock
    │   ├── dvc.yaml
    │   ├── mymodel.pkl    
    │   ├── my_script.py
    │   └── requirements.txt
    └── project_2
        ├── .dvc
        │   ├── config
        │   └── .gitignore
        └── .dvcignore
```
It is also assumed that artifacts are registered by [GTO](https://dvc.org/doc/gto) using a naming convention `project_name:artifact_name`, for example `gto register project_1:mymodel`.
(This naming convention is automatically followed when artifacts are registered from the DVC Studio UI).


The tool relies on `boto3` or `google-cloud-storage` to access the bucket (depending on the cloud storage used as a remote).

Right now, only a DVC remote which is at the root of a bucket is supported properly (i.e. no subdirectories)

### Usage

```cli
usage: dvcartifacts [-h] [-r REV] repourl projectdir artifact_name

Download an artifact from the remote bucket

positional arguments:
  repourl            url of the GitHub repository associated with the artifact
  projectdir         project subdirectory in the monorepo where the artifact was created
  artifact_name      Name of the artifact to find

options:
  -h, --help         show this help message and exit
  -r REV, --rev REV  semantic version of the artifact (optional), latest version is used if this is not specified
```