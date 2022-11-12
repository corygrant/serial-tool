"""
This file holds data model for MVC (Viewer/Controller Model) based application.
https://www.wildcardconsulting.dk/rdkit-gui-browser-with-mvc-using-pyside/
"""
from typing import List
from PyQt5 import QtCore

from serial_tool import defines as defs
from serial_tool import serComm


class SharedSignalsContainer:
    def __init__(self):
        self.sigWrite = None
        self.sigWarning = None
        self.sigError = None


class SerialToolSettings(QtCore.QObject):
    sigSerialSettingsUpdate = QtCore.pyqtSignal()
    sigDataFieldUpdate = QtCore.pyqtSignal(int)
    sigNoteFieldUpdate = QtCore.pyqtSignal(int)
    sigSeqFieldUpdate = QtCore.pyqtSignal(int)
    sigRxDisplayModeUpdate = QtCore.pyqtSignal()
    sigTxDisplayModeUpdate = QtCore.pyqtSignal()
    sigOutputRepresentationModeUpdate = QtCore.pyqtSignal()
    sigRxNewLineUpdate = QtCore.pyqtSignal()
    sigRxNewLineTimeoutUpdate = QtCore.pyqtSignal()

    def __init__(self):
        """
        Main shared data object.
        """
        super().__init__()

        self.serialSettings: serComm.SerialCommSettings = serComm.SerialCommSettings()

        self.configurationFilePath: str = None

        self.dataFields: List[str] = [""] * defs.NUM_OF_DATA_CHANNELS
        self.parsedDataFields: List[int] = [
            None
        ] * defs.NUM_OF_DATA_CHANNELS  # list of integers (bytes), as they are send over serial port
        self.noteFields: List[str] = [""] * defs.NUM_OF_DATA_CHANNELS
        self.seqFields: List[str] = [""] * defs.NUM_OF_SEQ_CHANNELS
        self.parsedSeqFields: List[SequenceData] = [None] * defs.NUM_OF_SEQ_CHANNELS  # list of parsed sequence blocks

        self.allRxTxData = []

        self.outputDataRepresentation = defs.OutputRepresentation.STRING
        self.displayReceivedData: bool = True
        self.displayTransmittedData: bool = True
        self.rxNewLine: bool = False
        self.rxNewLineTimeout: int = defs.DEFAULT_RX_NEWLINE_TIMEOUT_MS

    def setSerialSettings(self, serialSettings: serComm.SerialCommSettings):
        """
        Update serial settings and emit a signal at the end.
            @param serialSettings: new serial settings
        """
        self.serialSettings = serialSettings
        self.sigSerialSettingsUpdate.emit()

    def setDataField(self, channel: int, data: str):
        """
        Update data field and emit a signal at the end.
            @param channel: data channel index
            @param data: new data field string
        """
        self.dataFields[channel] = data
        self.sigDataFieldUpdate.emit(channel)

    def setNoteField(self, channel: int, data: str):
        """
        Update note field and emit a signal at the end.
            @param channel: note channel index
            @param data: new note field string
        """
        self.noteFields[channel] = data
        self.sigNoteFieldUpdate.emit(channel)

    def setSeqField(self, channel: int, data: str):
        """
        Update sequence field and emit a signal at the end.
            @param channel: sequence channel index
            @param data: new sequence field string
        """
        self.seqFields[channel] = data
        self.sigSeqFieldUpdate.emit(channel)

    def setRxDisplayMode(self, isEnabled: bool):
        """
        Update RX log visibility field and emit a signal at the end.
            @param isEnabled: if True, RX data is displayed in log.
        """
        self.displayReceivedData = isEnabled
        self.sigRxDisplayModeUpdate.emit()

    def setTxDisplayMode(self, isEnabled: bool):
        """
        Update TX log visibility field and emit a signal at the end.
            @param isEnabled: if True, TX data is displayed in log.
        """
        self.displayTransmittedData = isEnabled
        self.sigTxDisplayModeUpdate.emit()

    def setOutputRepresentationMode(self, outputRepresentation: int):
        """
        Update output representation field and emit a signal at the end.
            @param outputRepresentation: new output data representation mode.
        """
        self.outputDataRepresentation = outputRepresentation
        self.sigOutputRepresentationModeUpdate.emit()

    def setRxNewlineMode(self, isEnabled: bool):
        """
        Update RX new line field and emit a signal at the end.
            @param isEnabled: if True, new line is appended to RX data once received.
        """
        self.rxNewLine = isEnabled
        self.sigRxNewLineUpdate.emit()

    def setRxNewlineTimeout(self, timeoutMs: int):
        """
        Update RX new line timeout field and emit a signal at the end.
            @param timeoutMs: timeout after \n is appended to next RX data (if enabled).
        """
        self.rxNewLineTimeout = timeoutMs
        self.sigRxNewLineTimeoutUpdate.emit()


def _dataFieldIndexInRange(dataFieldIndex: int) -> bool:
    """
    Return True, if dataFieldIndex is in range: 0 - NUM_OF_DATA_CHANNELS, False otherwise.
    """
    if 0 >= dataFieldIndex < defs.NUM_OF_DATA_CHANNELS:
        return True
    else:
        return False


def _seqFieldIndexInRange(seqFieldIndex: int) -> bool:
    """
    Return True, if seqFieldIndex is in range: 0 - NUM_OF_SEQ_CHANNELS, False otherwise.
    """
    if 0 >= seqFieldIndex < defs.NUM_OF_SEQ_CHANNELS:
        return True
    else:
        return False
