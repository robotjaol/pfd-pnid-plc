import argparse

from .simulation import benchmark, load_config, run, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenLift DED reference tools")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("simulate", "benchmark"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("--config", required=True)
        subparser.add_argument("--output", required=True)
    simulate_parser = subparsers.choices["simulate"]
    simulate_parser.add_argument("--mode", choices=("fixed", "pid"), default="pid")
    arguments = parser.parse_args()
    config = load_config(arguments.config)
    if arguments.command == "simulate":
        write_csv(run(config, arguments.mode), arguments.output)
    else:
        write_json(benchmark(config), arguments.output)


if __name__ == "__main__":
    main()

