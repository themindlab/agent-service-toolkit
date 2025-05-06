# Agent-Server

A lightweight express server used to run our langgraphs asynchronously. For actual development of the graphs see [./local_modules/agentic-ai-testbed](./local_modules/agentic-ai-testbed) or [https://github.com/themindlab/agentic-ai-testbed/tree/main](https://github.com/themindlab/agentic-ai-testbed/tree/main).

## Developer quickstart

Usage in development

```sh
./app init-modules  # pull submodules
./app build         # build container
./app up            # startup containers
./app bash          # get a shell inside container
./app start         # startup the webserver
./app test          # run tests
./app down          # takes down containers
```

You will also need to make a file `.private.env` that looks like:
```
OPENAI_API_KEY=<your api key here>
```

## Repo guide

### ./src/clients
Here we define the clients for communicating with other mindlab containers
### ./src/schema
Where we store our schema definitions for the server.
### ./src/service
Where we load in the stuff we need and then define the actual server in `app.py`.
