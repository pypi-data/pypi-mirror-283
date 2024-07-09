# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in trainerliance with the License.
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
"""Contextmanager managing a gRPC channel to the Flower server."""


from contextlib import contextmanager
from logging import DEBUG, INFO, WARNING, ERROR
from queue import Queue
from typing import Callable, Iterator, Optional, Tuple, Any, Dict, List
from daisyflcocdrlib.common import FitRes, Status, Parameters, Code
from daisyflcocdrlib.utils.connection import grpc_connection

import grpc
from threading import Condition, Event, Lock

from daisyflcocdrlib.common import (
    HANDOVER,
    ROOT_CERTIFICATES,
    ANCHOR,
    GRPC_MAX_MESSAGE_LENGTH,
    CLIENT_IDLING,
    CLIENT_HANDLING,
    serde,
    ClientStatus,
    metadata_to_dict,
    dict_to_metadata,
)
from daisyflcocdrlib.common.logger import log
from daisyflcocdrlib.proto.transport_pb2 import ClientMessage, ServerMessage
from daisyflcocdrlib.proto.transport_pb2_grpc import FlowerServiceStub
from iterators import TimeoutIterator

# The following flags can be uncommented for debugging. Other possible values:
# https://github.com/grpc/grpc/blob/master/doc/environment_variables.md
# import os
# os.environ["GRPC_VERBOSITY"] = "debug"
# os.environ["GRPC_TRACE"] = "tcp,http"

def process_metadata(
    metadata: Tuple,
    anchor: Optional[str],
    root_certificates: Optional[bytes],
    handover: bool,
) -> Tuple:
    metadata_dict = metadata_to_dict(metadata, _check_reserved = False)
    
    if anchor is not None:
        metadata_dict[ANCHOR] = anchor
    elif metadata_dict.__contains__(ANCHOR):
        del metadata_dict[ANCHOR]
    
    if root_certificates is not None:
        metadata_dict[ROOT_CERTIFICATES] = root_certificates
    elif metadata_dict.__contains__(ROOT_CERTIFICATES):
        del metadata_dict[ROOT_CERTIFICATES]
    
    if handover:
        metadata_dict[HANDOVER] = "handover"
    elif metadata_dict.__contains__(HANDOVER):
        del metadata_dict[HANDOVER]
    
    return dict_to_metadata(metadata_dict)


class Z2MConnection:
    def __init__(self,
        # for grpc_connection
        parent_address: str = None,
        max_message_length: int = GRPC_MAX_MESSAGE_LENGTH,
        root_certificates: Optional[bytes] = None,
        metadata: Tuple = (),
        # sync up
        zone_entry = None,
    ):
        # transmission
        self.send: Callable = None
        self.receive: Callable = None
        # for grpc_connection
        self._parent_address: str = parent_address
        self._max_message_length: int = max_message_length
        self._root_certificates: Optional[bytes] = root_certificates
        self._metadata: Tuple = metadata
        self._anchor: str = None
        self.sleep_duration: int = 2
        # conditions
        self.event_disconn: Event = Event()
        self.event_disconn.set()
        self.event_reconn: Event = Event()
        self._cnd_api: Condition = Condition()
        self._busy: bool = False
        # sync up
        self._zone_entry = zone_entry
        # sentinel
        self.sentinel = ClientMessage(fit_res=serde.fit_res_to_proto(FitRes(
            status=Status(code=Code.OK, message="Success"),
            parameters=Parameters(tensors=[], tensor_type=""),
            config={},
        )))
        
    def run(self,):
        while True:
            # Wait for ZoneEntry ready and for reconnection
            log(DEBUG, "Connector idling")
            self.event_reconn.wait()
            log(DEBUG, "Connector reconnecting")
            try:
                with grpc_connection(self._parent_address, self._metadata, self._root_certificates) as conn:
                    send, receive = conn
                    self.receive = receive
                    self.send = send
                    # send ClientStatus
                    status_code = self._zone_entry.get_zone_entry_status_code()
                    if status_code == 1:
                        client_status = serde.client_status_to_proto(ClientStatus(status=CLIENT_IDLING))
                    elif status_code == 2:
                        client_status = serde.client_status_to_proto(ClientStatus(status=CLIENT_HANDLING))
                    else:
                        log(ERROR, "ZoneEntry should be closed.")
                    client_message = ClientMessage(client_status=client_status)
                    send(client_message)
                    # ZoneEntry can use
                    self.event_reconn.clear()
                    self.event_disconn.clear()
                    log(DEBUG, "ZoneEntry's term")
                    log(INFO, "Sleep for " + str(self.sleep_duration) + " seconds")
                    # Wait for ConnectionFail
                    self.event_disconn.wait()
                    log(DEBUG, "Connector's term")
                    Event().wait(timeout=self.sleep_duration)
            except:
                log(INFO, "Sleep for " + str(self.sleep_duration) + " seconds")
                Event().wait(timeout=self.sleep_duration)

    def set_anchor(self, reset: bool = True) -> None:
        if reset:
            self._anchor = None
        else:    
            self._anchor = self._parent_address

    def check_handover(self, ) -> bool:
        if (self._anchor is not None) and (self._parent_address is not None):
            if self._anchor != self._parent_address:
                return True
        return False


    # external APIs
    def reconnect(self,) -> bool:
        with self._cnd_api:
            while self._busy:
                self._cnd_api.wait()
            self._busy = True
        ###
        result = False
        if not self.event_disconn.is_set():
            log(
                WARNING,
                "Try reconnecting before disconnecting. " + \
                "Do nothing."
            )
        elif self.event_reconn.is_set():
            log(
                WARNING,
                "Another reconnection request has not been handled or the connection has not been built. " + \
                "Do nothing."
            )
        else:
            self.event_reconn.set()
            result = True
        ###
        self._busy = False
        with self._cnd_api:
            self._cnd_api.notify_all()
        return result

    def disconnect(self,) -> bool:
        with self._cnd_api:
            while self._busy:
                self._cnd_api.wait()
            self._busy = True
        ###
        result = False
        if self.event_disconn.is_set():
            log(
                WARNING,
                "Another disconnection request has not been handled or the connection has not been built. " + \
                "Do nothing."
            )
        else:
            self.event_disconn.set()
            result = True
        ###
        self._busy = False
        with self._cnd_api:
            self._cnd_api.notify_all()
        return result

    def handover(self, new_parent_address: str) -> None:
        with self._cnd_api:
            while self._busy:
                self._cnd_api.wait()
            self._busy = True
        ###
        if new_parent_address is not None:
            self._parent_address = new_parent_address
        ###
        self._busy = False
        with self._cnd_api:
            self._cnd_api.notify_all()

    def get_metadata(self,) -> Tuple:
        return self._metadata
    
def get_connector() -> Z2MConnection:
    _connector = None