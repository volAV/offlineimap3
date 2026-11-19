Upstream status (`master` branch):
[![OfflineIMAP build status on Travis-CI.org](https://travis-ci.org/OfflineIMAP/offlineimap.svg?branch=master)](https://travis-ci.org/OfflineIMAP/offlineimap)
[![OfflineIMAP code coverage on Codecov.io](https://codecov.io/gh/OfflineIMAP/offlineimap/branch/master/graph/badge.svg)](https://codecov.io/gh/OfflineIMAP/offlineimap)
[![Gitter chat](https://badges.gitter.im/OfflineIMAP/offlineimap.png)](https://gitter.im/OfflineIMAP/offlineimap)

Upstream status (`next` branch):
[![OfflineIMAP build status on Travis-CI.org](https://travis-ci.org/OfflineIMAP/offlineimap.svg?branch=next)](https://travis-ci.org/OfflineIMAP/offlineimap)

[offlineimap]: https://github.com/OfflineIMAP/offlineimap
[offlineimap3]: https://github.com/OfflineIMAP/offlineimap3
[website]: https://www.offlineimap.org
[wiki]: https://github.com/OfflineIMAP/offlineimap/wiki
[blog]: https://www.offlineimap.org/posts.html

Links:
* Official github code repository
  * for Python 2: [offlineimap]
  * for Python 3: [offlineimap3]
* Website: [website]
* Wiki: [wiki]
* Blog: [blog]

# OfflineIMAP

***"Get the emails where you need them."***


## Description

OfflineIMAP is software that downloads your email mailbox(es) as **local
Maildirs**. OfflineIMAP will synchronize both sides via *IMAP*.


## Why should I use OfflineIMAP?

IMAP's main downside is that you have to **trust** your email provider to
not lose your email. While certainly unlikely, it's not impossible.
With OfflineIMAP, you can download your Mailboxes and make you own backups of
your [Maildir](https://en.wikipedia.org/wiki/Maildir).

This allows reading your email offline without the need for your mail
reader (MUA) to support IMAP operations. Need an attachment from a
message without internet connection? No problem, the message is still there.


## Project status and future

OfflineIMAP, using Python 3, is based on OfflineIMAP for Python 2.
Currently we are updating the source code. These changes should not affect
the user (documentation, configuration files,... are the same) but some
links or packages could refer to the Python 2 version. In that case, please
open an issue.


## License

GNU General Public License v2.0 or later, with the existing OpenSSL exception;
see [COPYING](COPYING). Upstream attribution is retained.


## Downloads

You should first check if your distribution already packages OfflineIMAP for you.
Downloads releases as [tarball or zipball](https://github.com/OfflineIMAP/offlineimap3/tags).

If you are running Linux/BSD, you can install offlineimap with:

-  Debian and Ubuntu `apt install offlineimap3`
-  openSUSE `zypper install offlineimap`
-  Fedora `dnf install offlineimap`
-  FreeBSD `pkg search offlineimap3`, and install the python versioned package, `pkg install py311-offlineimap3`
-  Arch Linux: [`pacman -S offlineimap`](https://archlinux.org/packages/extra/any/offlineimap/), or through AUR package [offlineimap3-git](https://aur.archlinux.org/packages/offlineimap3-git/)
-  Docker image: `offlineimap/offlineimap:latest`
 (note: image not published yet, just an example)

### Isolated installation with pipx or UV

<!-- Modified 2026-11-19: document managed Python, pinned sources and installation verification. -->

With [UV](https://docs.astral.sh/uv/getting-started/installation/) available,
download a managed interpreter rather than using the operating system's Python:

```sh
uv python install 3.14
PYTHON="$(uv python find --managed-python 3.14)"
```

From the root of this checkout, choose **one** installer:

```sh
# pipx must already be available; it can itself be installed with:
# uv tool install --python "$PYTHON" pipx
pipx install --python "$PYTHON" .

# Alternatively:
uv tool install --python "$PYTHON" .
```

These commands install this checkout, not the PyPI distribution. The package is
still named `offlineimap` and provides the `offlineimap` command. Configuration
paths, including `~/.offlineimaprc`, are unchanged.

To install a fork without following a moving branch, replace `OWNER` and `COMMIT`
below with the fork owner and its full 40-character commit hash, then use one
installer:

```sh
SOURCE='git+https://github.com/OWNER/offlineimap3.git@COMMIT'
pipx install --python "$PYTHON" "$SOURCE"
# Alternatively:
uv tool install --python "$PYTHON" "$SOURCE"
```

Git must be available for these VCS URLs. A commit pins the application source,
not the interpreter patch release, build backend or transitive dependencies.
For repeated deployments, retain the tested wheel and record those versions.

Isolated builds require only `setuptools>=77.0.3`: setuptools reads the PEP 621
project metadata and supports the PEP 639 license expression and license files
(support introduced in 77.0.0). It also provides the wheel build command, so no
separate `wheel` requirement is needed. Source builds require Python 3.9 or newer
for this backend; the existing runtime Python metadata is unchanged. Runtime
dependencies are installed separately. Kerberos, keyring, Cygwin, SOCKS and
Internet-test dependencies remain opt-in extras, not build requirements.
Requesting Kerberos may require system Kerberos development tools.

#### Disposable verification

The following checks build an sdist and a wheel from that sdist with isolation
enabled, without replacing an existing tool installation:

```sh
CHECK="$(mktemp -d)"
export PIPX_HOME="$CHECK/pipx" PIPX_BIN_DIR="$CHECK/pipx-bin"
export PIPX_MAN_DIR="$CHECK/pipx-man"
export UV_TOOL_DIR="$CHECK/uv-tools" UV_TOOL_BIN_DIR="$CHECK/uv-bin"
uv build --python "$PYTHON" --out-dir "$CHECK/dist" .
pipx install --python "$PYTHON" "$CHECK"/dist/*.whl
uv tool install --python "$PYTHON" "$CHECK"/dist/*.whl
"$PIPX_BIN_DIR/offlineimap" --help
"$PIPX_BIN_DIR/offlineimap" --version
"$UV_TOOL_BIN_DIR/offlineimap" --help
"$UV_TOOL_BIN_DIR/offlineimap" --version
rm -rf "$CHECK"
unset PIPX_HOME PIPX_BIN_DIR PIPX_MAN_DIR UV_TOOL_DIR UV_TOOL_BIN_DIR
```

Verified on 2026-11-19 on Linux x86-64 with UV-managed CPython **3.14.10**,
pipx 1.4.3 and UV 0.13.9: isolated sdist/wheel build, both wheel installations,
`--help` and `--version` succeeded (`8.0.3`). Both distributions retained
`COPYING`; the wheel contained all 39 Python modules and the original console
entry point. Ordinary installations resolved distro 1.9.0, imaplib2 3.6 and
rfc6555 0.1.0, without Kerberos or other optional dependencies. imaplib2 3.6
emitted invalid-escape `SyntaxWarning`s on first import under Python 3.14.
This verifies installation and CLI startup only, not synchronization, optional
features, mail-server compatibility or other Python versions.

## Feedbacks and contributions

**The user discussions, development, announcements and all the exciting stuff take
place on the mailing list.** While not mandatory to send emails, you can
[subscribe here](http://lists.alioth.debian.org/mailman/listinfo/offlineimap-project).

Bugs, issues and contributions can be requested to both the mailing list or the
[official Github project][offlineimap3].  Provide the following information:
- system/distribution (with version)
- offlineimap version (`offlineimap -V`)
- Python version
- server name or domain
- CLI options
- Configuration file (offlineimaprc)
- pythonfile (if any)
- Logs, error
- Steps to reproduce the error


## The community

* OfflineIMAP's main site is the [project page at Github][offlineimap3].
* There is the [OfflineIMAP community's website][website].
* And finally, [the wiki][wiki].


## Requirements & dependencies

* Python v3.6+
* rfc6555 (required)
* imaplib2 >= 3.5 (required)
* keyring (optional), for storing passwords in a secure way
* gssapi (optional), for Kerberos authentication
* pysocks (optional), for proxy support
* portalocker (optional), if you need to run offlineimap in Cygwin for Windows
* certify (optional), for Internet SSL certificate validation
* urllib3 (optional), for Internet SSL certificate validation

## Documentation

All current and updated documentation is on the [community's website][website].


### Read documentation locally

You might want to read the documentation locally. Get the sources of the website.
For the other documentation, run the appropriate make target:

```sh
$ ./scripts/get-repository.sh website
$ cd docs
$ make html  # Requires rst2html
$ make man   # Requires a2x (http://asciidoc.org)
$ make api   # Requires sphinx
```

## UIDVALIDITY safety

This fork stops a folder sync immediately when an existing local or remote
UIDVALIDITY differs from the saved value. No messages are copied or uploaded, and
the synchronization status is not saved for that folder. Other folders can still
be processed, but the run reports the validity failure.

Do not overwrite the saved UIDVALIDITY for a nonempty mailbox. Back up the
affected Maildir and its state, download a fresh copy using a read-only remote
repository, and reconcile local-only messages and tags before switching state.

The isolated regression checks require no server or credentials:

```sh
python -B -m unittest test.tests.test_03_uidvalidity -v
```
