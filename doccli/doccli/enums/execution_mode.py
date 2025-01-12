from enum import StrEnum

class ExecutionMode(StrEnum):
    CLIENT = "client"
    SERVER = "server"
    CLIENT_SERVER = "client-server"