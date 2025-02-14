if [ $# -gt 0 ]; then

  if [ "$1" = "build" ]; then
    docker compose build --build-arg ENV="development" agent-server

  elif [ "$1" = "build_app" ]; then
    docker compose build --build-arg ENV="development" streamlit-app
  
  elif [ "$1" = "up" ]; then
    docker compose up -d

  elif [ "$1" = "ci_up" ]; then
    docker compose -f ./docker-compose.yaml --verbose up -d

  elif [ "$1" = "down" ]; then
    docker compose down
  
  elif [ "$1" = "start" ]; then
    docker compose exec agent-server python -u -m  run_service

  elif [ "$1" = "test" ]; then
    if [ ! -z "$2" ]; then
      shift 1
      docker compose exec -e PYTHONPATH=. \
        agent-server \
        pytest "$@"
    else
      docker compose exec -e PYTHONPATH=. \
        agent-server \
        pytest ./tests
    fi

  elif [ "$1" = "bash" ]; then
    docker compose exec -it agent-server bash
  
  elif [ "$1" = "init-modules" ]; then
    git submodule update --init --recursive --remote

  else
    echo "command not recognised"
  fi
else
  echo "No command supplied"
fi