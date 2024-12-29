# ⚠️ THIS PROJECT IS NOT YET READY TO BE USE

# DocCLI
DocCLI is a program that allows you to access your documentation from your CLI at any time.

## How it works

DocCLI is a two-part application:
- a **CLI** that can act as both a **client** and/or a **server**.
- a **backend** that serves as the **server**.

The purpose of this program is to read files from a local source or a remote source. These files can be stored on a hard drive or in a Git repository (S3 support is planned for the future).

**Note:** As of today, only the CLI component is ready to use; the backend component is still in development.

## Installation

// TODO

## Configuration

DocCLI is configured via environment variables, which can be set using a .env file or directly on the machine.

### Configuration common to client, server, and client-server mode
- `DOCCLI_MODE`: Defines whether the program is run in
    - `client-server` mode, acting as both the retriever and reader of files.

    - `client` mode, acting as the one requesting access to files (**not yet implemented.**)

    - `server` mode, handling file retrieval and managing authentication-related systems (**not yet implemented.**)

- `DOCCLI_SOURCE`: This variable accepts `os` or `git` as parameters to indicate if files should be retrieved from an external source (Git, S3...) or accessed directly on the machine (os).

- `DOCCLI_BASE_DIR`: Defines the base path for file searches.
    - If the `DOCCLI_SOURCE` value is `os`, the program will use the value as the base directory for file searches. For example, if `DOCCLI_BASE_DIR` is set to "/", searching for foo.txt will locate the file at the equivalent of /foo.txt in Linux.

    - If `DOCCLI_SOURCE` is not `os`, the value should point to an empty folder that will serve as the destination for cloned content. For example, if the source is `git`, the Git repository will be cloned and stored locally.

#### Git-Specific Configuration
If `DOCCLI_SOURCE` is set to `git`, you can configure the following variables:
- `GIT_URL`: The URL of the Git repository
- `GIT_BRANCH`: The Git branch to monitor
- `GIT_USERNAME`: The Git username (required if the Git repository is private, **not yet implemented**)
- `GIT_PASSWORD`: The Git authentication token, used as a password (required if the Git repository is private, **not yet implemented**)

**Note:** If you use DocCLI's Git features, Git must be installed on the machine running the application.

### Client-Mode Specific Configuration

- `DOCCLI_SERVER_URL`: **not yet implemented**
- `DOCCLI_TOKEN`: **not yet implemented**

### Backend Mode-Specific Configuration

- `DOCCLI_AUTHENTICATION_ENABLE`: **not yet implemented**
- `DOCCLI_SERVER_PORT`: **not yet implemented**
- `DOCCLI_TOKEN_DURATION`: **not yet implemented**

## Start the Program

To start the program, use `doccli` in your terminal.

```bash
$ doccli --help
```

## Commands

### Search

`search` is the main command. It allows you to search for a file, view its contents, or display a directory tree.

```bash
# View the contents of a file
$ DOCCLI_BASE_DIR=/my-base-folder DOCCLI_MODE=os doccli search /foo.txt
> hello world

# View the contents of a folder
$ DOCCLI_BASE_DIR=/my-base-folder DOCCLI_MODE=os doccli search /foo
.
└── awesome-file.md
```