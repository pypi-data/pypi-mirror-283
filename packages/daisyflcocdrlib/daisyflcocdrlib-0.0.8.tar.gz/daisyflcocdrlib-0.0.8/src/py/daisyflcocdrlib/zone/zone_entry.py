from queue import Queue
from logging import INFO, DEBUG, ERROR
from daisyflcocdrlib.common.logger import log
from typing import Callable, Dict, Optional, Union, Tuple, List
from threading import Lock, Event
from daisyflcocdrlib.proto.transport_pb2 import ClientMessage, ServerMessage
from .grpc_client.message_handler import handle
from enum import Enum
from daisyflcocdrlib.utils.task_manager import TaskManager
from daisyflcocdrlib.common import (
    Status,
    Code,
    Parameters,
    serde,
    ClientUploadingSignal,
    SERVER_WAITING,
    SERVER_IDLING,
    FitRes,
)

class ZoneEntryStatus(Enum):
    RECEIVING = 1
    SENDING = 2
    CLOSE = 3

class ZoneEntry:
    def __init__(
        self,
        task_manager: TaskManager,
    ) -> None:
        self._status: ZoneEntryStatus = ZoneEntryStatus.RECEIVING
        self._lock_status: Lock = Lock()
        self._event_stop: Event = Event()
        self._shutdown: bool = False
        self._server_message: Optional[ServerMessage] = None
        self._client_message: Optional[ClientMessage] = None
        self._task_manager: TaskManager = task_manager
    
    def run(self,) -> None:
        while not self._shutdown:
            # TODO: MTFL, while(receive) -> create a thread for handling and sending
            self._receiving()
            self._handling()
            self._sending()
        
    def _receiving(self,) -> None:
        while True:
            if self._status.value != 1:
                log(INFO, "Skip receiving")
                return None
            success = self._handle_connection(1)
            if not success:
                return None
            log(DEBUG, "ZoneEntry tries receiving message")
            try:
                server_message, _ = self._connector.receive()
                self._connector.set_anchor(reset=False)
                with self._lock_status:
                    self._server_message = server_message
                    if self._status.value != 3:
                        self._status = ZoneEntryStatus.SENDING
                    self._event_stop.clear()
                    ### === ###
                    """for loose association"""
                    self._connector.disconnect()
                    ### === ###
            except:
                log(DEBUG, "Reset Connection")
                self._connector.disconnect()
                self._connector.reconnect()
    
    def _handling(self,) -> None:
        if self._status.value != 2:
            log(INFO, "Skip handling")
            return None
        # TODO: Stop after Event.set()
        log(DEBUG, "ZoneEntry tries handling ServerMessage")
        server_message: ServerMessage = self._server_message
        self._client_message = handle(server_message, self._task_manager)
        self._server_message = None

    def _sending(self,) -> None:
        while True:
            if self._status.value != 2:
                log(INFO, "Skip sending")
                return None
            success = self._handle_connection(2)
            if not success:
                return None
            log(DEBUG, "ZoneEntry tries sending message")
            try:
                # send CUS
                cus = ClientUploadingSignal(status=Status(code=Code.OK, message=""))
                cus_msg = ClientMessage(client_uploading_signal=serde.client_uploading_signal_to_proto(cus))
                self._connector.send(cus_msg)
                log(DEBUG, "Send CUS")
                # receive ServerStatus
                server_status_msg, ss_success = self._connector.receive()
                if not ss_success:
                    return None
                if server_status_msg.WhichOneof("msg") != "server_status":
                    return None
                server_status = serde.server_status_from_proto(server_status_msg.server_status)
                if server_status.status == SERVER_WAITING:
                    server_waiting = True
                elif server_status.status == SERVER_IDLING:
                    server_waiting = False
                else:
                    return None
                log(DEBUG, "Receive ServerStatus")
                # IF: server waiting, send the result
                if server_waiting:
                    client_message: ClientMessage = self._client_message
                # IF: server idling, send a sentinel
                else:
                    client_message: ClientMessage = ClientMessage(fit_res=serde.fit_res_to_proto(FitRes(
                        status=Status(code=Code.OK, message="Success"),
                        parameters=Parameters(tensors=[], tensor_type=""),
                        config={},
                    )))
                self._connector.send(client_message)
                log(DEBUG, "Result uploaded")
                # receive SRS
                server_message, _ = self._connector.receive() # SRS
                log(DEBUG, "Receive SRS")
                self._connector.set_anchor(reset=True)
                with self._lock_status:
                    if self._status.value != 3:
                        self._client_message = None
                        self._status = ZoneEntryStatus.RECEIVING
                    ### === ###
                    """for loose association"""
                    self._connector.disconnect()
                    ### === ###
                return None
            except:
                log(DEBUG, "Reset Connection")
                self._connector.disconnect()
                self._connector.reconnect()

    def _handle_connection(self, status_code: int) -> bool:
        while True:
            if self._status.value != status_code:
                return False
            # TODO: use condition to prevent busy waiting
            event_dis = self._connector.event_disconn.is_set()
            event_rec = self._connector.event_reconn.is_set()
            if (not event_dis) and (not event_rec):
                # Connection Ready
                return True
            elif (event_dis) and (not event_rec):
                log(INFO, "Send reconnection request")
                self._connector.reconnect()
                Event().wait(timeout=1)
            elif (event_dis) and (event_rec):
                log(INFO, "Wait for reconnecting")
                Event().wait(timeout=1)
            else:
                log(ERROR, "Wait for reconnecting before disconnecting. It shouldn't happen.")

    # register functions
    def set_connector(
        self,
        connector,
    ) -> None:
        self._connector = connector

    # APIs
    def get_zone_entry_status_code(self,) -> int:
        return self._status.value

    def shutdown(self,) -> None:
        self._shutdown = True
        with self._lock_status:
            self._status = ZoneEntryStatus.CLOSE
            # break from the current function
            self._connector.disconnect()
            self._event_stop.set()
        return
