# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from logging import INFO, WARNING, ERROR
from typing import Dict, List, Optional, Tuple, TypedDict, Callable
from queue import Queue
from threading import Event
from daisyflcocdrlib.operator.strategy import Strategy
from daisyflcocdrlib.common import (
    Parameters,
    Report,
    Task,
    CURRENT_ROUND,
    TIMEOUT,
    PERIOD,
    CREDENTIAL,
    TID, 
)
from daisyflcocdrlib.common.logger import log

from daisyflcocdrlib.operator.utils import (
    get_configure_fit,
    aggregate_fit,
    generate_fit_report,
    get_configure_evaluate,
    aggregate_evaluate,
    generate_evaluate_report,
    wait_for_results,
)


class ServerLogic():
    def __init__(self,
        server,
        strategy: Strategy,
    ) -> None:
        self.server = server
        self.strategy: Strategy = strategy
        self.subtasks = {}

    def fit_round(
        self,
        parameters: Parameters,
        task: Task,
    ) -> Optional[
        Tuple[Optional[Parameters], Optional[Report]]
    ]:
        """Perform a single round fit."""
        # Get clients and their respective instructions from strategy
        ## credential
        if CREDENTIAL in task.config:
            credential = task.config[CREDENTIAL]
        else:
            log(ERROR, "\"{}\" is a required key in a Task.".format(CREDENTIAL))
        ## get_clients
        client_instructions = get_configure_fit(
            strategy=self.strategy,
            server_round=task.config[CURRENT_ROUND],
            parameters=parameters,
            server=self.server,
            config=task.config,
            credential=credential,
        )
        # Collect `fit` results from all clients participating in this round
        subtask_id = self.server.fit_clients(
            client_instructions=client_instructions,
            max_workers=self.server.get_max_workers(),
            timeout=task.config[TIMEOUT],
        )
        self.subtasks[subtask_id] = subtask_id
        Event().wait(timeout=task.config[PERIOD])
        # check
        results = []
        for stid in list(self.subtasks.values()):
            results = results + self.server.get_results(stid)
        results_roaming = self.server.get_results_roaming(tid=task.config[TID], fit=True)
        results = results + results_roaming
        if len(results) == 0:
            return parameters, generate_fit_report(task.config, 0, {},)
        # Aggregate training results
        parameters_aggregated, samples, metrics_aggregated = aggregate_fit(
            strategy=self.strategy,
            server_round=task.config[CURRENT_ROUND],
            results=results,
            failures=[],
        )
        # Get report
        report = generate_fit_report(
            task_config=task.config,
            samples=samples,
            metrics_aggregated=metrics_aggregated,
        )

        return parameters_aggregated, report

    def evaluate_round(
        self,
        parameters: Parameters,
        task: Task,
    ) -> Optional[Report]:
        """Validate current global model on a number of clients."""
        # Get clients and their respective instructions from strategy
        ## credential
        if CREDENTIAL in task.config:
            credential = task.config[CREDENTIAL]
        else:
            log(ERROR, "\"{}\" is a required key in a Task.".format(CREDENTIAL))
        ## get_clients
        client_instructions = get_configure_evaluate(
            strategy=self.strategy,
            server_round=task.config[CURRENT_ROUND],
            parameters=parameters,
            server=self.server,
            config=task.config,
            credential=credential,
        )
        # Collect `evaluate` results from all clients participating in this round
        subtask_id = self.server.evaluate_clients(
            client_instructions=client_instructions,
            max_workers=self.server.get_max_workers(),
            timeout=task.config[TIMEOUT],
        )
        # check
        success = wait_for_results(strategy=self.strategy, current_returns=self.server.get_current_returns(subtask_id))
        if not success:
            return generate_evaluate_report(task.config, 0, 9999.0, {},)
        results = self.server.get_results(subtask_id)
        results_roaming = self.server.get_results_roaming(tid=task.config[TID], fit=False)
        results = results + results_roaming
        self.server.finish_subtask(subtask_id)
        # Aggregate the evaluation results
        loss_aggregated, samples, metrics_aggregated = aggregate_evaluate(
            strategy=self.strategy,
            server_round=task.config[CURRENT_ROUND],
            results=results,
            failures=[],
        )
        # Get report
        report = generate_evaluate_report(
            task_config=task.config,
            samples=samples,
            loss_aggregated=loss_aggregated,
            metrics_aggregated=metrics_aggregated,
        )

        return report
