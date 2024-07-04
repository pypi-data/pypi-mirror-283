"""
    QApp Platform Project braket_circuit_export_task.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from braket.circuits import Circuit
from qbraid import circuit_wrapper

from qapp_common.async_tasks.export_circuit_task import CircuitExportTask
from qapp_common.config.logging_config import logger
from qapp_common.enum.sdk import Sdk


class BraketCircuitExportTask(CircuitExportTask):

    def _transpile_circuit(self):
        logger.debug("[BraketCircuitExportTask] _transpile_circuit()")

        circuit = self.circuit_data_holder.circuit

        if isinstance(circuit, Circuit):
            return circuit_wrapper(circuit).transpile(Sdk.QISKIT.value)

        raise Exception("Invalid circuit type!")
