from time import sleep
from db.model import Config
from db.api_db import add_config, update_config, get_config
import pygatt

def saveConfigurationBT(self):
    if not self.mac_bt:
        return

    DATA_TO_SEND = []

    # self.label_statusESP.setText("Desconectado")
    # SEND CONFIG TO ESP
    Status = self.STATUS_DICT[self.operationModeBox.currentText()]
    ID_Protocol = int(self.protocolIDBox.currentText())
    val_boxes = [
        int(self.AccSamplingBox.toPlainText()).to_bytes(4, 'big'),
        int(self.AccSensibilityBox.toPlainText()).to_bytes(4, 'big'),
        int(self.GyroSensibilityBox.toPlainText()).to_bytes(4, 'big'),
        int(self.BME688SamplingBox.toPlainText()).to_bytes(4, 'big'),
        int(self.discontinuosTimeBox.toPlainText()).to_bytes(4, 'big'),
        int(self.portTCPBox.toPlainText()).to_bytes(4, 'big'),
        int(self.portUDPBox.toPlainText()).to_bytes(4, 'big'),
        int(self.hostIPAddrBox.toPlainText()).to_bytes(4, 'big'),
    ]

    for idx, val_box in enumerate(val_boxes):
        esp_data = (
            bytearray((3).to_bytes(1, 'big')) +
            bytearray((idx+3).to_bytes(1, 'big')) +
            bytearray(val_box)
        )
        DATA_TO_SEND.append(esp_data)

    val_boxex_text = [
        bytes(self.ssidBox.toPlainText(), 'utf-8'),
        bytes(self.passBox.toPlainText(), 'utf-8'),
    ]

    for idx, val_box in enumerate(val_boxex_text):
        esp_data_2 = (
            bytearray((4).to_bytes(1, 'big')) +
            bytearray((idx+11).to_bytes(1, 'big')) +
            bytearray(val_box)
        )
        DATA_TO_SEND.append(esp_data_2)

    # SAVE DATA IN DB
    self.consoleLog("Saving configuration...")
    lastConfig = get_config(self.mac)

    if lastConfig.count() == 1:
        try:
            new_config = {
                "Status": Status,
                "ID_Protocol": ID_Protocol,
                "BMI270_sampling": int(self.AccSamplingBox.toPlainText()),
                "BMI270_Acc_Sensibility": int(self.AccSensibilityBox.toPlainText()),
                "BMI270_Gyro_Sensibility": int(self.GyroSensibilityBox.toPlainText()),
                "BME688_Sampling": int(self.BME688SamplingBox.toPlainText()),
                "Discontinuous_Time": int(self.discontinuosTimeBox.toPlainText()),
                "Port_TCP": int(self.portTCPBox.toPlainText()),
                "Port_UDP": int(self.portUDPBox.toPlainText()),
                "Host_Ip_Addr": int(self.hostIPAddrBox.toPlainText()),
                "Ssid": self.ssidBox.toPlainText(),
                "Pass": self.passBox.toPlainText(),
            }

        except:
            self.consoleLog("Wrong configuration inputs")
        if update_config(self.mac, new_config):
            DATA_TO_SEND.append(bytearray([2, Status, ID_Protocol]))
            self.consoleLog("Configuration saved")
        else:
            self.consoleLog("Error saving configuration")
    else:
        try:
            configs = Config(
                mac = self.mac,
                Status = Status,
                ID_Protocol = ID_Protocol,
                BMI270_sampling = int(self.AccSamplingBox.toPlainText()),
                BMI270_Acc_Sensibility = int(self.AccSensibilityBox.toPlainText()),
                BMI270_Gyro_Sensibility = int(self.GyroSensibilityBox.toPlainText()),
                BME688_Sampling = int(self.BME688SamplingBox.toPlainText()),
                Discontinuous_Time = int(self.discontinuosTimeBox.toPlainText()),
                Port_TCP = int(self.portTCPBox.toPlainText()),
                Port_UDP = int(self.portUDPBox.toPlainText()),
                Host_Ip_Addr = int(self.hostIPAddrBox.toPlainText()),
                Ssid = self.ssidBox.toPlainText(),
                Pass = self.passBox.toPlainText(),
            )
        except:
            self.consoleLog("Wrong configuration inputs")
        if add_config(configs):
            self.consoleLog("Configuration saved")
            DATA_TO_SEND.append(bytearray([2, Status, ID_Protocol]))
        else:
            self.consoleLog("Error saving configuration")

    # SELECT PROTOCOL FOR PLOTS
    self.setProtocol(ID_Protocol)

    # CONNECT TO BT
    adapter = pygatt.backends.GATTToolBackend()
    for data in DATA_TO_SEND:
        while True:
            try:
                adapter.start()
                device = adapter.connect(self.mac_bt)
                device.exchange_mtu(60)
                device.char_write(self.deviceUUID, data)
                break
            except:
                sleep(1)
            finally:
                adapter.stop()
    self.consoleLog("BT CONFIG: Sended data full")

def saveConfigurationWIFI(self):
    Status = self.STATUS_DICT[self.operationModeBox.currentText()]
    ID_Protocol = int(self.protocolIDBox.currentText())
    self.consoleLog("Saving configuration...")
    lastConfig = get_config(self.mac)

    if lastConfig.count() == 1:
        try:
            new_config = {
                "Status": Status,
                "ID_Protocol": ID_Protocol,
                "BMI270_sampling": int(self.AccSamplingBox.toPlainText()),
                "BMI270_Acc_Sensibility": int(self.AccSensibilityBox.toPlainText()),
                "BMI270_Gyro_Sensibility": int(self.GyroSensibilityBox.toPlainText()),
                "BME688_Sampling": int(self.BME688SamplingBox.toPlainText()),
                "Discontinuous_Time": int(self.discontinuosTimeBox.toPlainText()),
                "Port_TCP": int(self.portTCPBox.toPlainText()),
                "Port_UDP": int(self.portUDPBox.toPlainText()),
                "Host_Ip_Addr": int(self.hostIPAddrBox.toPlainText()),
                "Ssid": self.ssidBox.toPlainText(),
                "Pass": self.passBox.toPlainText(),
            }

        except:
            self.consoleLog("Wrong configuration inputs")
        if update_config(self.mac, new_config):
            self.consoleLog("Configuration saved")
        else:
            self.consoleLog("Error saving configuration")
    else:
        try:
            configs = Config(
                mac = self.mac,
                Status = Status,
                ID_Protocol = ID_Protocol,
                BMI270_sampling = int(self.AccSamplingBox.toPlainText()),
                BMI270_Acc_Sensibility = int(self.AccSensibilityBox.toPlainText()),
                BMI270_Gyro_Sensibility = int(self.GyroSensibilityBox.toPlainText()),
                BME688_Sampling = int(self.BME688SamplingBox.toPlainText()),
                Discontinuous_Time = int(self.discontinuosTimeBox.toPlainText()),
                Port_TCP = int(self.portTCPBox.toPlainText()),
                Port_UDP = int(self.portUDPBox.toPlainText()),
                Host_Ip_Addr = int(self.hostIPAddrBox.toPlainText()),
                Ssid = self.ssidBox.toPlainText(),
                Pass = self.passBox.toPlainText(),
            )
        except:
            self.consoleLog("Wrong configuration inputs")
        if add_config(configs):
            self.consoleLog("Configuration saved")
        else:
            self.consoleLog("Error saving configuration")

    # SELECT PROTOCOL FOR PLOTS
    self.setProtocol(ID_Protocol)

def saveConfiguration(self):
    if self.label_statusESP.text() == "Conectado UDP/TCP":
        print("CONFIGURATION WIFI")
        saveConfigurationWIFI(self)
    else:
        print("CONFIGURATION BT")
        saveConfigurationBT(self)