if __name__ == '__main__':
    from .download import download_version
    import plac
    import sys

    commands = {
        "download": download_version,
    }

    if len(sys.argv) == 1:
        print("Available commands:", ", ".join(commands))
        sys.exit(1)

    command = sys.argv.pop(1)

    if command in commands:
        plac.call(commands[command], sys.argv[1:])
    else:
        print("Unknown command:", command)
        print("Available commands:", ", ".join(commands))
        sys.exit(1)
