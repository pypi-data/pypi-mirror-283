import warnings

from ..application_base import JupyterKernelsBaseApp


class KernelLogoutApp(JupyterKernelsBaseApp):
    """An application to logout of a remote kernel provider."""

    description = """
      An application to logout of a remote kernel provider.

      jupyter kernels logout
    """

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 0:  # pragma: no cover
            warnings.warn("Too many arguments were provided for logout.")
            self.print_help()
            self.exit(1)

        self._fetch(
            "{}/api/iam/v1/logout".format(self.cloud_base_url),
        )
        self._log_out()
        self.log.info("Successfully logged out.")
