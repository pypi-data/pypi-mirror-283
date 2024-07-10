# rdfc

Convert RDF files to any serialization format via [rdflib](https://github.com/RDFLib/rdflib)

## Installation

Install using `pip`:

```shell
$ pip install git+https://github.com/svenrdz/rdfc
```

## Examples

```shell
$ rdfc file.jsonld ttl
Triples written to ~/file.ttl
```

```shell
$ rdfc file.jsonld /tmp/output.n3
Triples written to /tmp/output.n3
```

```shell
$ rdfc file.jsonld ttl
Triples written to ~/file.ttl

$ rdfc file.jsonld file.ttl
Output file exists already ~/file.ttl
Aborted.

$ rdfc file.jsonld file.ttl --force
Output file exists already ~/ws/file.ttl
Overriding since `--force` is used.
Triples written to ~/ws/file.ttl
```

## Help

```shell
$ rdfc --help

 Usage: rdfc [OPTIONS] INPUT OUTPUT_OR_FORMAT

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    input                 PATH  [default: None] [required]                                              │
│ *    output_or_format      TEXT  [default: None] [required]                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --force                 --no-force      [default: no-force]                                              │
│ --install-completion                    Install completion for the current shell.                        │
│ --show-completion                       Show completion for the current shell, to copy it or customize   │
│                                         the installation.                                                │
│ --help                                  Show this message and exit.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
