# DocCLI

*An easy way to read documentation hosted on a remote server or a Git repository through your terminal.*

DocCLI is a program designed to allow reading files from the terminal. The files can be located in different storage options, whether on an OS filesystem, a Git repository, or in the future, on S3, SharePoint, OneDrive, and more.

## Highlights
- Makes it easy to access and read files located on different hosts, all from a single CLI.
- Supports multiple storage options: Filesystem, Git Repository, and in the future, S3, SharePoint, OneDrive, and more.
- Allows reading files such as `.doc`, `.pdf`, `.xlsx`...

## Installation
There are two ways to install DocCLI:

### Installation script
In the "script" folder, there are two installation scripts for the project:
- `install.sh` to install DocCLI on a Unix system.
- `install.bat` to install DocCLI on Windows.

### From release
You can install the Python program directly from the GitHub Release tab. However, you will need to manually add it to your environment to invoke it using `doccli`.

### Check if everything is working
To verify that everything is set up correctly, you can use the command `doccli --help` or `doccli --version`.

## Configuration

The application has three operating modes:
- `client-server` mode: Acts as both the retriever and reader of files. Useful for local testing.
- `client` mode: Requests access to files and folders.
- `server` mode: Handles file retrieval and manages authentication-related systems (**authentication is not yet implemented**).

Currently, the application is exclusively configurable through environment variables.

### Common configuration

| Environment variable name | Possible values | Default | Description |
| ---                       | ---             | ---     | ---         |
| DOCCLI_MODE | `client-server`, `client`, or `server` | `` | Defines in which mode the program should run. |

### Client configuration
If `DOCCLI_MODE` is `client`
| Environment variable name | Possible values | Default | Description |
| ---                       | ---             | ---     | ---         |
| DOCCLI_ENDPOINT | URL; `http://url-to-doccli-server`, `https://url-to-doccli-server` | `` | Defines the URL of the DocCLI endpoint. This endpoint is a DocCLI instance running in `server` mode. |

### Server configuration
If `DOCCLI_MODE` is `server` or `client-server`
| Environment variable name | Possible values | Default | Description |
| ---                       | ---             | ---     | ---         |
| DOCCLI_SOURCE | `os`, `git` | `` | Defines the data source—whether it should be retrieved from an external source (Git, S3...) or accessed directly on the machine (OS). |
| DOCCLI_BASE_DIR | Path; `/tmp/my-doc`, `/some/kind/of/folder`, `C:/some/kind/of/folder` | `` | Defines the path that will contain the documentation. If DOCCLI_SOURCE is `os`, it is the directory where the documents are located. In other cases, it is an empty folder that will hold a copy of the data extracted from the source. |

### Git Source configuration 
If `DOCCLI_SOURCE` is `git`:
| Environment variable name | Possible values | Default | Description |
| ---                       | ---             | ---     | ---         |
| GIT_URL | URL; `https://url-to-github-project`, `https://url-to-gitlab-project`... | `` | The URL of the Git repository. |
| GIT_BRANCH | String; `main`, `master`, `develop`... | `` | The name of the branch DocCLI is monitoring. |
| GIT_USERNAME | String; `bob`, `robert`... | `` | The Git username (required if the Git repository is private, **not yet implemented**). |
| GIT_PASSWORD | String; `kitty`, `admin`... | `` | The Git authentication token, used as a password (required if the Git repository is private, **not yet implemented**). |

**Note:** If you use DocCLI's Git features, Git must be installed on the machine running the application.

## Start the Program

To start the program, use `doccli` in your terminal.

```bash
$ doccli --help
```

## Commands

### Search

`search` is the main command. It allows you to search for a file, view its contents, or display a list of folders and files

```bash
# View the contents of a file
$ DOCCLI_BASE_DIR=/my-base-folder DOCCLI_MODE=os doccli search /foo.txt
> "-------------- START CONTENT --------------"
> hello world
> "--------------- END CONTENT ---------------"
```

```bash
# View the contents of a folder
$ DOCCLI_BASE_DIR=/my-base-folder DOCCLI_MODE=os doccli search /foo
    awesome-file.md
    my-super-folder/
    how-to-be-rich.pdf
    i-am-poor.xlsx
    Go back
    Quit

# The folder section is a screen where you can freely select any option
```