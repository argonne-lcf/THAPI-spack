#!/usr/bin/env python3
r"""Declare a system LLVM as a Spack external that satisfies h2yaml.

h2yaml needs ``llvm@18:+clang+python``, where ``+python`` means the prefix ships
clang's Python bindings (``clang/cindex.py``) next to ``libclang``. Two things make
this awkward to set up by hand:

* ``spack external find`` picks variants from executables and never looks for the
  bindings, so it always records LLVM as ``~python`` -- which cannot satisfy h2yaml,
  leaving the system LLVM unused.
* Distributions split the pieces up (Debian keeps the bindings in
  ``/usr/lib/python3/dist-packages``, far from ``/usr/lib/llvm-N``) and site installs
  are usually read-only, so the bindings often cannot be dropped in place.

This script resolves both. It locates the bindings, and if they live outside the LLVM
prefix -- or are missing entirely, in which case they are fetched from the matching
LLVM release, since they are pure Python -- it builds an *overlay* prefix: a tree of
symlinks to the real install plus a ``site-packages`` holding the bindings. It then
prints the ``packages.yaml`` config pointing at whichever prefix is usable.

The config is printed on stdout, so it can be redirected or piped straight into Spack::

    python3 scripts/gen-llvm-external.py /usr/lib/llvm-18          # just look at it
    python3 scripts/gen-llvm-external.py /usr/lib/llvm-18 > ext.yaml && spack config add -f ext.yaml
    spack config add -f <(python3 scripts/gen-llvm-external.py /usr/lib/llvm-18)

Pass ``--python-version`` to match the python Spack will run h2yaml with; it defaults
to the running python. Any overlay is created under ``--overlay-dir`` and must be
kept, since the external points into it.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import textwrap
import urllib.error
import urllib.request
from pathlib import Path

# The bindings are two or three plain .py files. enumerations.py was dropped after
# LLVM 18, so it is fetched only if the tag actually has it.
BINDINGS_REQUIRED = ("__init__.py", "cindex.py")
BINDINGS_OPTIONAL = ("enumerations.py",)
RAW_URL = "https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-{version}/clang/bindings/python/clang/{name}"

# Overlays must outlive the command, since the Spack external points into one.
# ~/.spack is where the packages.yaml referring to it lives, so they travel together.
DEFAULT_OVERLAY_DIR = Path("~/.spack")


def die(msg):
    sys.exit(f"error: {msg}")


def llvm_version(prefix):
    """Full x.y.z version of the LLVM at *prefix*, via its own llvm-config."""
    llvm_config = prefix / "bin" / "llvm-config"
    if not llvm_config.is_file():
        die(f"no llvm-config in {prefix}/bin -- is that really an LLVM prefix?")
    raw = subprocess.check_output([str(llvm_config), "--version"], universal_newlines=True).strip()
    # Strip suffixes such as "19.1.7git", which are not release tags.
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)", raw)
    if not m:
        die(f"cannot parse llvm-config --version output {raw!r}")
    return m.group(0), int(m.group(1))


def find_bindings(*roots):
    """Directory containing ``clang/cindex.py``, searched over usual layouts."""
    for root in roots:
        if root is None or not root.is_dir():
            continue
        for libdir in ("lib", "lib64"):
            base = root / libdir
            if not base.is_dir():
                continue
            for pydir in sorted(base.glob("python*")):
                for pkgs in ("site-packages", "dist-packages"):
                    if (pydir / pkgs / "clang" / "cindex.py").is_file():
                        return pydir / pkgs
        # Debian: /usr/lib/python3/dist-packages, with no python<X.Y> level.
        for pkgs in root.glob("lib/python3/dist-packages"):
            if (pkgs / "clang" / "cindex.py").is_file():
                return pkgs
    return None


def fetch_bindings(version, dest):
    """Download clang's pure-python bindings for *version* into ``dest/clang``."""
    out = dest / "clang"
    out.mkdir(parents=True, exist_ok=True)
    for name in BINDINGS_REQUIRED + BINDINGS_OPTIONAL:
        url = RAW_URL.format(version=version, name=name)
        try:
            with urllib.request.urlopen(url) as r:
                (out / name).write_bytes(r.read())
        except (urllib.error.URLError, OSError) as e:
            if name in BINDINGS_OPTIONAL:
                continue
            die(f"cannot fetch {name} from llvmorg-{version} ({e}) -- is that a real release tag?")
    return out.parent


def build_overlay(llvm, overlay, bindings, py_version):
    """Symlink *llvm* into *overlay*, with *bindings* exposed on Spack's python path.

    The real install is usually read-only, so nothing is copied into it: every entry
    is symlinked, except ``lib`` which is recreated as a real directory so the
    bindings can be added alongside the symlinked libraries.
    """
    if overlay.exists():
        shutil.rmtree(overlay)
    (overlay / "lib").mkdir(parents=True)
    for entry in llvm.iterdir():
        if entry.name != "lib":
            (overlay / entry.name).symlink_to(entry)
    for entry in (llvm / "lib").iterdir():
        (overlay / "lib" / entry.name).symlink_to(entry)

    site = overlay / "lib" / f"python{py_version}" / "site-packages"
    site.parent.mkdir(parents=True, exist_ok=True)
    if bindings is None:
        version, _ = llvm_version(llvm)
        site.mkdir()
        fetch_bindings(version, site)
    else:
        site.symlink_to(bindings)
    return overlay


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("prefix", type=Path, help="system LLVM prefix, e.g. /usr/lib/llvm-18")
    p.add_argument(
        "--overlay-dir",
        type=Path,
        default=DEFAULT_OVERLAY_DIR,
        help=f"where to create the overlay, if one is needed. It must keep existing for as long as Spack uses the external (default: {DEFAULT_OVERLAY_DIR})",
    )
    p.add_argument("--python-version", help="python X.Y Spack runs h2yaml with (default: this interpreter)")
    args = p.parse_args()

    llvm = args.prefix.resolve()
    version, major = llvm_version(llvm)
    if major < 18:
        die(f"h2yaml needs llvm@18: but {llvm} is {version}")

    py_version = args.python_version or f"{sys.version_info.major}.{sys.version_info.minor}"

    # Bindings already inside the prefix: usable as-is, no overlay.
    bindings = find_bindings(llvm)
    if bindings and str(bindings).startswith(str(llvm) + os.sep):
        prefix, note = llvm, f"bindings found in {bindings}"
    else:
        # Otherwise look where distributions put them, then fall back to fetching.
        bindings = find_bindings(Path("/usr"), Path("/usr/local"))
        overlay = args.overlay_dir.expanduser() / f"llvm-{version}-overlay"
        prefix = build_overlay(llvm, overlay.resolve(), bindings, py_version)
        note = f"bindings from {bindings}" if bindings else f"bindings fetched from llvmorg-{version}"

    if not find_bindings(prefix):
        die(f"no clang/cindex.py under {prefix} after setup -- refusing to write a +python external that would fail later")

    # `llvm+clang` provides c/cxx, so Spack may pick this external as the compiler
    # for the whole build. That only works if the entry carries the compiler paths --
    # spack's own llvm package treats `compilers` as mandatory for a detected llvm.
    # Without them Spack still selects it, then builds with SPACK_CC=None and every
    # compile dies with "C compiler cannot create executables".
    #
    # Which compiler to build THAPI with is a separate decision, left to whoever runs
    # the install (e.g. `spack install thapi %gcc`); this file only makes the external
    # usable and correct.
    cc, cxx = prefix / "bin" / "clang", prefix / "bin" / "clang++"
    for path in (cc, cxx):
        if not path.exists():
            die(f"{path} is missing -- an llvm external with +clang must provide it")

    yaml = textwrap.dedent(f"""\
        packages:
          llvm:
            externals:
            - spec: llvm@{version}+clang+python
              prefix: {prefix}
              extra_attributes:
                compilers:
                  c: {cc}
                  cxx: {cxx}
            buildable: false
        """)
    # The config goes to stdout so it can be piped straight into Spack; everything
    # else is progress info and belongs on stderr.
    print(f"llvm@{version}: {note}", file=sys.stderr)
    if prefix != llvm:
        print(f"created overlay {prefix} (keep it: the external points here)", file=sys.stderr)
    print(yaml, end="")


if __name__ == "__main__":
    main()
