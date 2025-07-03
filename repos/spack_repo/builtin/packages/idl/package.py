# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Idl(Package):
    """IDL Software: Interactive Data Visualization.

    Note: IDL is a licensed software. You will also need an existing
    downloaded tarball of IDL in your current directory or in a
    spack mirror in order to install."""

    homepage = "https://www.nv5geospatialsoftware.com/Products/IDL"
    manual_download = True

    maintainers("LRWeber")

    version(
        "9.1", sha256="4889100ae314577fd0139a962084df3cfb43209d0b34877cbba03e8d010146c9"
    )
    version(
        "9.0", sha256="8faf7ec8091ee77e6297f91a823e5c6216f2ab90909071955bec008c268b0f62"
    )

    # Licensing
    license_required = True
    license_url = "https://www.nv5geospatialsoftware.com/docs/idl-install.html"

    patch("install.patch", when="@9.0")

    def url_for_version(self, version):
        url = "file://{0}/idl{1}-linux.tar.gz".format(
            os.getcwd(), str(version).replace(".", "")
        )
        return url

    def install(self, spec, prefix):
        # replace default install dir to self.prefix by editing answer file
        os.chmod("silent/idl_answer_file", 0o644)
        filter_file("/usr/local/nv5", prefix, "silent/idl_answer_file")

        # execute install script
        install_script = Executable("./install.sh")
        install_script("-s", input="silent/idl_answer_file")

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        # add bin to path
        env.prepend_path("PATH", self.prefix.idl.bin)
