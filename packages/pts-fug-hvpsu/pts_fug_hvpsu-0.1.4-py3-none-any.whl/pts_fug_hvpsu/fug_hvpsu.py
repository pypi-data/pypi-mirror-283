import logging
import time
import socket


class FugHVPsu:
    """
    ``Base class for the FUG HV PSU``
    """
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    def __init__(self, connection_string, port):
        self.connection_string = connection_string
        self.port = port
        self.sock = None
        self.upper_voltage_limit = 1000  # Defaults to 1000V, needs to be compatible with the System if changed

    def open_connection(self):
        """
        ``Opens a TCP/IP connection to connect to the FUG HV PSU``
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.connection_string, self.port))
            logging.info(f": Opening FUG HV PSU connection at {self.connection_string} and port {self.port}")
        except Exception as e:
            raise Exception(f": ERROR {e}: Could not open connection")

    def close_connection(self):
        """
        ``Closes the TCP/IP connection to the FUG HV PSU``
        """
        self.sock.close()
        logging.info(": Closing TCP/IP connection!")

    def query_data(self):
        """
        ``This command queries the FuG PSU identity data`` \n
        :return: `str` : PSU Data
        """
        self.sock.send(b'? \n')
        time.sleep(0.3)
        query_data = self.sock.recv(1024)
        logging.info(f": Data: {query_data.decode()}")
        return str(query_data.decode())

    def clear_device(self):
        """
        ``This command clears the initialization data.`` \n
        :return: `str` : Error code for the command
        """
        self.sock.send(b'= \n')
        time.sleep(0.3)
        clr = self.sock.recv(1024).decode().rstrip()
        if clr == 'E0':
            logging.info(f": Cleared Device: {clr}")
            return str(clr)
        else:
            raise Exception(f": ERROR {clr}: Clearing device ")

    def identification_number(self):
        """
        ``This command checks the identification number`` \n
        :return: `str` : Identification number
        """
        self.sock.send(b'*IDN? \n')
        time.sleep(0.3)
        idn = self.sock.recv(1024)
        logging.info(f": Identification number: {idn.decode()}")
        return str(idn.decode())

    def enable_output(self):
        """
        ``This command enables the output`` \n
        :return: `str` : Error code for the command
        """
        self.sock.send(b'F1 \n')
        time.sleep(0.3)
        op_on = str(self.sock.recv(1024).decode().rstrip())
        if op_on == 'E0':
            logging.info(f": Output Enabled: {op_on}")
            return str(op_on)
        else:
            raise Exception(f": ERROR {op_on}: Enabling output ")

    def disable_output(self):
        """
        ``This command disables the output`` \n
        :return: `str` : Error code for the command
        """
        self.sock.send(b'F0 \n')
        time.sleep(0.3)
        op_off = self.sock.recv(1024).decode().rstrip()
        if op_off == 'E0':
            logging.info(f": Output Disabled: {op_off}")
            return str(op_off)
        else:
            raise Exception(f": ERROR {op_off}: Disabling output")

    def set_voltage(self, volt: float):
        """
        ``This command will set the output voltage in Volts`` \n
        :param volt: output voltage in Volts [Range: 0-2000V] \n
        :return: `str` : Error code for the command [E0 is No Error]
        """
        if volt > self.upper_voltage_limit:
            raise ValueError(f" WARNING: Voltage exceeding {self.upper_voltage_limit}V is not permitted. Please adjust your input.")
        else:
            b_volt = 'U'+str(volt)
            self.sock.send(b_volt.encode()+b'\n')
            time.sleep(0.3)
            voltage = self.sock.recv(1024).decode().rstrip()
            if voltage == 'E0':
                logging.info(f": Voltage set: {voltage}")
                return str(voltage)
            else:
                raise Exception(f": ERROR {voltage}: Setting Voltage ")

    def set_current(self, curr_limit: float):
        """
        ``This command will set the output current in Amps`` \n
        :param curr_limit: current limit in Amps [0-6 mA] \n
        :return: `str` : Error code for the command [E0 is No Error]
        """
        b_curr = 'I'+str(curr_limit)
        self.sock.send(b_curr.encode()+b'\n')
        time.sleep(0.3)
        current = self.sock.recv(1024).decode().rstrip()
        if current == 'E0':
            logging.info(f": Current limit set: {current}")
            return str(current)
        else:
            raise Exception(f": ERROR {current}: Setting Current limit ")

    def measure_voltage(self):
        """
        ``This function measures output voltage`` \n
        :return: `float` : Programmed output voltage in Volts
        """
        self.sock.send(b'>M0? \n')
        meas_volt = self.sock.recv(1024).decode().rstrip().split(":")[-1]
        logging.info(f": Output Voltage: {meas_volt} Volts")
        return float(meas_volt)

    def measure_current(self):
        """
        ``This function measures output current`` \n
        :return: `float` : Programmed output Current in milliAmps
        """
        self.sock.send(b'>M1? \n')
        meas_curr = self.sock.recv(1024).decode().rstrip().split(":")[-1]
        logging.info(f": Output Current: {meas_curr} Amps")
        return float(meas_curr)
