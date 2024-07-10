from pathlib import Path
from typing import Annotated

from rdflib import Graph
from rich import print
from typer import Abort, Exit, Option, Typer

app = Typer()

FORMATS = dict(
    ttl="turtle",
    n3="nt",
    nt="nt",
    xml="pretty-xml",
    trix="trix",
    trig="trig",
    n4="nquads",
    jsonld="json-ld",
    hext="hext",
)


def tilde(p: Path) -> str:
    home = str(Path.home())
    absol = p.absolute().as_posix()
    if absol.startswith(home):
        absol = absol.replace(home, "~")
    return absol


@app.command()
def convert(
    input: Path,
    output_or_format: Path,
    force: Annotated[
        bool,
        Option(
            "--force",
            "-f",
            help="Allow overriding files",
        ),
    ] = False,
):
    if not input.is_file():
        print(f"Input file does not exist: {tilde(input)}")
        raise Abort
    output: Path
    if output_or_format.suffix == "":
        suffix = str(output_or_format)
        output = input.with_suffix(f".{suffix}")
    else:
        suffix = output_or_format.suffix[1:]
        output = Path(output_or_format)
    if suffix not in FORMATS:
        print(f"Unknown serialization format: {suffix}")
        raise Abort
    if output.is_file():
        print(f"Output file exists already {tilde(output)}")
        if force:
            print("Overriding since `--force` is used.")
        else:
            raise Abort
    g = Graph()
    g.parse(input)
    g.serialize(output, format=FORMATS[suffix])
    print(f"Triples written to {tilde(output)}")


if __name__ == "__main__":
    app()
