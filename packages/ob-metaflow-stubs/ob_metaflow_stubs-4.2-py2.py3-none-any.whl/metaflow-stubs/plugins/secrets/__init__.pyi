##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.7.1+nim(0.0.1);ob(v1)                                         #
# Generated on 2024-07-08T23:52:24.940462                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import abc

class SecretsProvider(abc.ABC, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None) -> typing.Dict[str, str]:
        """
        Retrieve the secret from secrets backend, and return a dictionary of
        environment variables.
        """
        ...
    ...

