from collections.abc import Mapping

import atoti as tt
from atoti._external_table_identifier import ExternalTableIdentifier
from atoti.directquery._external_database_connection import (
    ExternalDatabaseConnection,
)
from typing_extensions import override

from .table import DatabricksTable


class DatabricksConnection(ExternalDatabaseConnection[DatabricksTable]):
    """Connection to an external Databricks database.

    See Also:
        :class:`~atoti_directquery_databricks.DatabricksConnectionInfo`.
    """

    @override
    def _create_table(
        self,
        identifier: ExternalTableIdentifier,
        /,
        *,
        types: Mapping[str, tt.DataType],
    ) -> DatabricksTable:
        return DatabricksTable(identifier, database_key=self._database_key, types=types)

    def _update_connection_string_and_password(
        self, /, *, connection_string: str, password: str
    ) -> None:
        self._java_api.external_api(
            self._database_key
        ).updateConnectionStringAndPassword(connection_string, password)
