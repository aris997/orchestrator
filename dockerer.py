from python_on_whales import DockerClient, docker

docker = DockerClient(compose_files=['path to the /docker-compose.yml'])

docker.compose.up(detach=True)

for container in docker.compose.ps():
    if 'db' in container.name:
        print(container, container.name)
        fname = container.name + '.sql.backup'
        docker.execute(container, ["pg_dump", "postgres", "-f", "/var/lib/postgresql/" + fname])
        docker.copy((container, "/var/lib/postgresql/" + fname), fname)
