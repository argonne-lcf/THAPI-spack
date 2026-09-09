#!/usr/bin/env python3
r"""Declare a system package as a Spack external, with the version read from a tool.

``spack external find`` only detects packages whose recipe declares ``executables``
or ``libraries`` -- 172 of ~8900 in the builtin repo. Everything else has to be
declared by hand, even when it is plainly installed: ``re2c`` and ``protobuf`` are
both apt packages that Spack will otherwise spend ~15 minutes each rebuilding.

This writes the ``packages.yaml`` entry for one such package. The version comes from
running the tool itself, so the config cannot drift from what is actually installed::

    python3 scripts/gen-external.py re2c --version-from re2c
    python3 scripts/gen-external.py protobuf --version-from protoc

The config is printed on stdout, so it can be redirected or piped into Spack::

    python3 scripts/gen-external.py re2c --version-from re2c > ext.yaml
    spack config add -f ext.yaml

Pass ``--version`` instead of ``--version-from`` when there is no tool to ask, and
``--prefix`` when the package does not live in ``/usr``.

Note this only writes the config. Whether Spack actually picks the external up
depends on the version satisfying what depends on it -- check with ``spack spec``,
which marks an external ``[e]``.

For LLVM use ``gen-llvm-external.py`` instead: h2yaml needs a ``+python`` variant
whose bindings distributions scatter outside the prefix, which needs real work
beyond writing a version and a path.
"""

import argparse
import re
import subprocess
import sys
import textwrap


def die(msg):
    sys.exit(f"error: {msg}")


def version_from_tool(tool):
    """First dotted version in ``<tool> --version`` output.

    Covers the usual shapes without a per-tool rule: "re2c 3.1",
    "libprotoc 3.21.12", "cmake version 3.28.3".
    """
    try:
        out = subprocess.check_output(
            [tool, "--version"], universal_newlines=True, stderr=subprocess.STDOUT
        )
    except OSError as e:
        die(f"cannot run {tool} --version ({e}) -- is it installed and on PATH?")
    except subprocess.CalledProcessError as e:
        die(f"{tool} --version failed with status {e.returncode}:\n{e.output}")
    m = re.search(r"\d+(?:\.\d+)+", out)
    if not m:
        die(f"no version found in {tool} --version output:\n{out}")
    return m.group(0)


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("package", help="Spack package name, e.g. re2c")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--version-from", metavar="TOOL", help="read the version from `TOOL --version`")
    g.add_argument("--version", help="use this version verbatim")
    p.add_argument("--prefix", default="/usr", help="install prefix (default: /usr)")
    p.add_argument(
        "--buildable",
        action="store_true",
        help="let Spack build the package too. By default it may not, so a version that stops"
        " satisfying its dependents fails the solve instead of silently rebuilding from source",
    )
    p.add_argument(
        "--variants",
        default="",
        help="variants to append to the spec, e.g. '+shared'. Only add what is actually true of"
        " the installed package: Spack trusts the spec and will not verify it",
    )
    args = p.parse_args()

    version = args.version or version_from_tool(args.version_from)
    spec = f"{args.package}@{version}{args.variants}"

    yaml = textwrap.dedent(f"""\
        packages:
          {args.package}:
            externals:
            - spec: {spec}
              prefix: {args.prefix}
            buildable: {str(args.buildable).lower()}
        """)
    # The config goes to stdout so it can be piped straight into Spack; everything
    # else is progress info and belongs on stderr.
    print(f"{spec}: prefix {args.prefix}", file=sys.stderr)
    print(yaml, end="")


if __name__ == "__main__":
    main()
