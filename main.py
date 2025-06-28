import os
from python_on_whales import DockerClient
from datetime import datetime


def backup_database(compose_path: str = "docker-compose.yml"):
    """Create a backup of the database using Docker Compose"""
    docker = DockerClient(compose_files=[compose_path])

    docker.compose.up(detach=True)

    for container in docker.compose.ps():
        if 'db' in container.name.lower():
            print(f"Creating backup for {container.name}")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            fname = f"{container.name}_{timestamp}.sql"

            docker.execute(container, ["pg_dump", "postgres", "-f", f"/var/lib/postgresql/{fname}"])

            docker.copy((container, f"/var/lib/postgresql/{fname}"), fname)
            print(f"Backup created: {fname}")


def list_backups():
    """List all backup files"""
    backup_files = [f for f in os.listdir(os.path.join('.')) if f.endswith('.sql')]
    if backup_files:
        print("Available backups:")
        for backup in sorted(backup_files):
            print(f"  - {backup}")
    else:
        print("No backups found")


def main():
    print("Orchestrator - Backup Service")
    
    if len(os.sys.argv) > 1:
        command = os.sys.argv[1]
        
        if command == "backup":
            compose_path = os.sys.argv[2] if len(os.sys.argv) > 2 else "docker-compose.yml"
            backup_database(compose_path)
        elif command == "list":
            list_backups()
        else:
            print("Available commands: backup [compose-path], list")
    else:
        print("Usage: python main.py <command>")
        print("Commands:")
        print("  backup [compose-path] - Create database backup")
        print("  list                  - List available backups")


if __name__ == "__main__":
    main()
