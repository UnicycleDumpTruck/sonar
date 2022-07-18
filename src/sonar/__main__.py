"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Sonar."""


if __name__ == "__main__":
    main(prog_name="sonar")  # pragma: no cover
