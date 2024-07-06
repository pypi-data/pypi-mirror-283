import threading
import serial
import numpy as np
import serial.tools.list_ports
import serial.threaded
import datetime

comm = None
conn = None
reader = None

global debug
debug = False

global triggerLevel
triggerLevel = 100


class Protocol(object):
    def connection_made(self, transport):
        """연결이 성립되었을 때 호출되는 메서드입니다.

        Args:
            transport: 연결된 트랜스포트 객체
        """

    def data_received(self, data):
        """데이터를 수신했을 때 호출되는 메서드입니다.

        Args:
            data: 수신된 데이터
        """

    def connection_lost(self, exc):
        """연결이 끊어졌을 때 호출되는 메서드입니다.

        Args:
            exc: 예외 객체, 연결이 정상적으로 끊어진 경우 None
        """
        if isinstance(exc, Exception):
            raise exc


class ReaderThread(threading.Thread):
    def __init__(self, serial_instance, protocol_factory):
        """ReaderThread 초기화 메서드입니다.

        Args:
            serial_instance: 시리얼 인스턴스
            protocol_factory: 프로토콜 팩토리 함수
        """
        super(ReaderThread, self).__init__()
        self.daemon = True
        self.serial = serial_instance
        self.protocol_factory = protocol_factory
        self.alive = True
        self._lock = threading.Lock()
        self._connection_made = threading.Event()
        self.protocol = None

    def stop(self):
        """스레드를 중지시키는 메서드입니다."""
        self.alive = False
        if hasattr(self.serial, 'cancel_read'):
            self.serial.cancel_read()
        self.join(2)

    def run(self):
        """스레드 실행 메서드입니다."""
        if not hasattr(self.serial, 'cancel_read'):
            self.serial.timeout = 1
        self.protocol = self.protocol_factory()
        try:
            self.protocol.connection_made(self)
        except Exception as e:
            self.alive = False
            self.protocol.connection_lost(e)
            self._connection_made.set()
            return
        error = None
        self._connection_made.set()
        while self.alive and self.serial.is_open:
            try:
                data = self.serial.read(self.serial.in_waiting or 1)
            except serial.SerialException as e:
                error = e
                break
            else:
                if data:
                    try:
                        self.protocol.data_received(data)
                    except Exception as e:
                        error = e
                        break
        self.alive = False
        self.protocol.connection_lost(error)
        self.protocol = None

    def write(self, data):
        """데이터를 시리얼 포트로 쓰는 메서드입니다.

        Args:
            data: 전송할 데이터
        """
        with self._lock:
            self.serial.write(data)

    def close(self):
        """시리얼 포트를 닫는 메서드입니다."""
        with self._lock:
            self.stop()
            self.serial.close()

    def connect(self):
        """연결을 시도하는 메서드입니다.

        Returns:
            tuple: (self, self.protocol)
        """
        if self.alive:
            self._connection_made.wait()
            if not self.alive:
                raise RuntimeError('connection_lost already called')
            return (self, self.protocol)
        else:
            raise RuntimeError('already stopped')

    def __enter__(self):
        """컨텍스트 매니저 진입 메서드입니다."""
        self.start()
        self._connection_made.wait()
        if not self.alive:
            raise RuntimeError('connection_lost already called')
        return self.protocol

    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료 메서드입니다."""
        self.close()


class raw_protocol(Protocol):
    def __init__(self):
        """raw_protocol 초기화 메서드입니다."""
        self.transport = None
        self.running = True
        self.buffer = np.array([], dtype=np.uint8)
        self.in1 = 255
        self.in2 = 255
        self.in3 = 255
        self.in4 = 255
        self.remocon = 255

    # 연결 시작시 발생
    def connection_made(self, transport):
        """연결이 성립되었을 때 호출되는 메서드입니다.

        Args:
            transport: 연결된 트랜스포트 객체
        """
        self.transport = transport
        self.running = True
        self.buffer = np.array([], dtype=np.uint8)
        self.in1 = 255
        self.in2 = 255
        self.in3 = 255
        self.in4 = 255
        self.triggerLevel = 100
        self.remocon = 255

    # 연결 종료시 발생
    def connection_lost(self, exc):
        """연결이 끊어졌을 때 호출되는 메서드입니다.

        Args:
            exc: 예외 객체, 연결이 정상적으로 끊어진 경우 None
        """
        self.transport = None
        self.buffer = None
        self.in1 = 255
        self.in2 = 255
        self.in3 = 255
        self.in4 = 255
        self.triggerLevel = 100
        self.remocon = 255

    #데이터가 들어오면 이곳에서 처리함.
    def data_received(self, data):
        """데이터를 수신했을 때 호출되는 메서드입니다.

        Args:
            data: 수신된 데이터
        """
        self.buffer = np.append(self.buffer, np.frombuffer(data, dtype=np.uint8))
        while len(self.buffer) >= 3:
            if self.buffer[0] == 0x23:
                length = self.buffer[1]
                total_length = length + 3  # 시작 바이트, 길이 바이트, 체크섬 포함
                if len(self.buffer) >= total_length:
                    packet = self.buffer[:total_length]
                    self.buffer = self.buffer[total_length:]
                    self.handle_packet(packet)
                else:
                    break
            else:
                self.buffer = self.buffer[1:]

    # 패킷 핸들
    def handle_packet(self, packet):
        """패킷을 처리하는 메서드입니다.

        Args:
            packet: 처리할 패킷
        """
        try:
            self.in1, self.in2, self.in3, self.in4, self.remocon = self.parse_data(packet)
        except ValueError as e:
            raise ValueError("Invalid parsing data")

    # 파싱 데이터
    def parse_data(self, data):
        """데이터를 파싱하는 메서드입니다.

        Args:
            data: 파싱할 데이터

        Returns:
            tuple: (in1, in2, in3, in4, remocon)
        """
        if len(data) < 11:
            raise ValueError("Invalid data length")

        start_byte, length, cmd = data[0], data[1], data[2]
        if len(data) != length + 3:
            raise ValueError("Invalid data length")

        in1, in2, in3, in4, remocon, checksum = data[3], data[4], data[5], data[6], data[9], data[10]

        if start_byte != 0x23:
            raise ValueError("Invalid start byte")
        calc_checksum = 0
        for byte in data[2:-1]:
            calc_checksum ^= byte
        if calc_checksum != checksum:
            raise ValueError("Invalid checksum")

        return in1, in2, in3, in4, remocon

    # 디지털 입력 1 읽기
    def get_digit_in1(self):
        """PIN 1의 HIGH, LOW 값으로 데이터를 읽습니다.

        Returns:
            digital in1
        """
        global triggerLevel
        if self.in1 < triggerLevel:
            return 0
        else:
            return 1

    # 디지털 입력 2 읽기
    def get_digit_in2(self):
        """PIN 2의 HIGH, LOW 값으로 데이터를 읽습니다.

        Returns:
            digital in2
        """
        global triggerLevel
        if self.in2 < triggerLevel:
            return 0
        else:
            return 1

    # 디지털 입력 3 읽기
    def get_digit_in3(self):
        """PIN 3의 HIGH, LOW 값으로 데이터를 읽습니다.

        Returns:
            digital in3
        """
        global triggerLevel
        if self.in3 < triggerLevel:
            return 0
        else:
            return 1

    # 디지털 입력 4 읽기
    def get_digit_in4(self):
        """PIN 4의 HIGH, LOW 값으로 데이터를 읽습니다.

        Returns:
            digital in4
        """
        global triggerLevel
        if self.in4 < triggerLevel:
            return 0
        else:
            return 1

    # 아날로그 입력 1 읽기
    def get_analog_in1(self):
        """PIN 1의 ADC 값으로 데이터를 읽습니다.

        Returns:
            analog in1
        """
        return self.in1

    # 아날로그 입력 2 읽기
    def get_analog_in2(self):
        """PIN 2의 ADC 값으로 데이터를 읽습니다.

        Returns:
            analog in2
        """
        return self.in2

    # 아날로그 입력 3 읽기
    def get_analog_in3(self):
        """PIN 3의 ADC 값으로 데이터를 읽습니다.

        Returns:
            analog in3
        """
        return self.in3

    # 아날로그 입력 4 읽기
    def get_analog_in4(self):
        """PIN 4의 ADC 값으로 데이터를 읽습니다.

        Returns:
            analog in4
        """
        return self.in4

    # 리모컨 읽기
    def get_remocon(self):
        """리모컨의 데이터를 읽습니다.

        Returns:
            remocon
        """
        return self.remocon

    # 데이터 보낼 때 함수
    def write(self, data):
        """시리얼로 데이터를 전송합니다.

        Args:
            data: 파싱할 데이터
        """
        self.transport.write(data)

    # 종료 체크
    def isDone(self):
        """쓰레드 종료 상태를 반환합니다.

        Returns:
            쓰레드 상태
        """
        return self.running


def get_serial_list():
    """시리얼 포트의 리스트를 반환합니다.

    Returns:
       시리얼 포트 리스트
    """
    ports = serial.tools.list_ports.comports()
    for port in ports:
        _printf(f"포트: {port.device}, 설명: {port.description}, 하드웨어 ID: {port.hwid}")
    return ports


def open(port, baud):
    """시리얼 포트를 연결합니다.

    Args:
        port: 포트 문자열
        baud: 통신속도

    Returns:
        conn: 연결된 쓰레드를 반환
        reader: 읽은 데이터 확인을 위한 프로토콜 리더 반환
    """
    global comm, reader, conn
    comm = serial.serial_for_url(port, baud, timeout=1)
    if comm is not None:
        _printf(f"통신포트 연결 성공")
    reader = raw_protocol()
    conn = ReaderThread(comm, lambda: reader)
    conn.start()
    return conn, reader


def gpio_out(pin, logic):
    """GPIO 출력을 설정합니다.

    Args:
        pin: 출력할 핀 번호
        logic: 출력 (0: low, 1: high)

    Returns:
        boolean: 전송 성공 여부
    """
    logic_min = 0
    logic_max = 1
    pin_min = 1
    pin_max = 6

    if not _check_serial():
        _printf(f"통신포트가 연결되어있지 않습니다.")
        return False
    if not (logic_min <= logic <= logic_max):
        _printf(f"GPIO 출력은 {logic_min} 부터 {logic_max} 사이의 값만 허용됩니다.")
        return False
    if not (pin_min <= pin <= pin_max):
        _printf(f"GPIO의 핀은 {pin_min}부터 {pin_max} 사이의 값만 허용됩니다.")
        return False

    if pin >= 1:
        pin = pin - 1
    buf = _make_buf(0x80, pin, logic)
    sendbuf = bytearray(buf)
    _printf(f"전송 버퍼: {buf}")
    comm.write(sendbuf)
    return True


def servo_motor(pin, angle, speed):
    """서버모터 동작을 설정합니다.

    Args:
        pin: 서버모터 동작 핀 번호 (3 ~ 6)
        angle: 각도를 설정합니다. (-90 ~ 90)
        speed: 속도를 설정합니다. (0 ~ 30)
    Returns:
        boolean: 전송 성공 여부
    """
    angle_min = -90
    angle_max = 90
    pin_min = 3
    pin_max = 6
    speed_min = 0
    speed_max = 30

    if pin >= 1:
        pin = pin -1

    if not _check_serial():
        _printf(f"통신포트가 연결되어있지 않습니다.")
        return False
    if not (pin_min <= pin <= pin_max):
        _printf(f"GPIO 핀은 {pin_min} 부터 {pin_max} 사이의 값만 허용됩니다.")
        return False
    if not (speed_min <= speed <= speed_max):
        _printf(f"속도는 {speed_min} 부터 {speed_max} 사이의 값만 허용됩니다.")
        return False
    if not (angle_min <= angle <= angle_max):
        _printf(f"각도는 {angle_min} 부터 {angle_max} 사이의 값만 허용됩니다.")
        return False

    buf = _make_buf(0x81, pin, angle, speed)
    sendbuf = bytearray(buf)
    _printf(f"전송 버퍼: {buf}")
    comm.write(sendbuf)
    return True


def dc_motor_all_on(l1, r1, l2, r2):
    """DC모터1,2를 동작 시킵니다.

    Args:
        l1: L1의 속도를 설정합니다. (-100 ~ 100)
        l2: L2의 속도를 설정합니다. (-100 ~ 100)
        r1: R1의 속도를 설정합니다. (-100 ~ 100)
        r2: R2의 속도를 설정합니다. (-100 ~ 100)
    Returns:
        boolean: 전송 성공 여부
    """
    speed_min = -100
    speed_max = 100

    if not _check_serial():
        _printf(f"통신포트가 연결되어있지 않습니다.")
        return False
    if not (speed_min <= l1 <= speed_max):
        _printf(f"L1의 속도는 {speed_min} 부터 {speed_max} 사이의 값만 허용됩니다.")
        return False
    if not (speed_min <= l2 <= speed_max):
        _printf(f"L2의 속도는 {speed_min} 부터 {speed_max} 사이의 값만 허용됩니다.")
        return False
    if not (speed_min <= r1 <= speed_max):
        _printf(f"R1의 속도는 {speed_min} 부터 {speed_max} 사이의 값만 허용됩니다.")
        return False
    if not (speed_min <= r2 <= speed_max):
        _printf(f"R2의 속도는 {speed_min} 부터 {speed_max} 사이의 값만 허용됩니다.")
        return False

    buf = _make_buf(0x82, l1, r1, l2, r2)
    sendbuf = bytearray(buf)
    _printf(f"전송 버퍼: {buf}")
    comm.write(sendbuf)
    return True


def dc_motor_all_off():
    """DC모터1,2를 동작을 중지합니다.

    Returns:
        boolean: 전송 성공 여부
    """
    if not _check_serial():
        print(f"통신포트가 연결되어있지 않습니다.")
        return False
    buf = _make_buf(0x83)
    sendbuf = bytearray(buf)
    _printf(f"전송 버퍼: {buf}")
    comm.write(sendbuf)
    return True


def dc_motor1_on(l1, r1):
    """DC모터1를 동작 시킵니다.

    Args:
        l1: L1의 속도를 설정합니다. (-100 ~ 100)
        r1: R1의 속도를 설정합니다. (-100 ~ 100)

    Returns:
        boolean: 전송 성공 여부
    """
    speed_min = -100
    speed_max = 100

    if not _check_serial():
        _printf(f"통신포트가 연결되어있지 않습니다.")
        return False
    if not (speed_min <= l1 <= speed_max):
        _printf(f"L1의 속도는 {speed_min} 부터 {speed_max} 사이의 값만 허용됩니다.")
        return False
    if not (speed_min <= r1 <= speed_max):
        _printf(f"R1의 속도는 {speed_min} 부터 {speed_max} 사이의 값만 허용됩니다.")
        return False

    buf = _make_buf(0x85, l1, r1)
    sendbuf = bytearray(buf)
    _printf(f"전송 버퍼: {buf}")
    comm.write(sendbuf)
    return True


def dc_motor2_on(l2, r2):
    """DC모터2를 동작 시킵니다.

    Args:
        l2: L2의 속도를 설정합니다. (-100 ~ 100)
        r2: R2의 속도를 설정합니다. (-100 ~ 100)

    Returns:
        boolean: 전송 성공 여부
    """
    speed_min = -100
    speed_max = 100

    if not _check_serial():
        _printf(f"통신포트가 연결되어있지 않습니다.")
        return False
    if not (speed_min <= l2 <= speed_max):
        _printf(f"L2의 속도는 {speed_min} 부터 {speed_max} 사이의 값만 허용됩니다.")
        return False
    if not (speed_min <= r2 <= speed_max):
        _printf(f"R2의 속도는 {speed_min} 부터 {speed_max} 사이의 값만 허용됩니다.")
        return False

    buf = _make_buf(0x86, l2, r2)
    sendbuf = bytearray(buf)
    _printf(f"전송 버퍼: {buf}")
    comm.write(sendbuf)
    return True


def set_debug(state):
    """디버그 출력을 설정합니다.

    Args:
        state: True: 라이브러리 출력모드를 켭니다., False: 라이브러리 출력모드를 끕니다.

    """
    global debug
    debug = state


def set_digit_in_trigger(level):
    """디지털 입력의 트리거 레벨을 설정합니다.
    Args:
        level: ADC값을 0과 1로 표현하기 위한 트리거 레벨입니다. 0~255 범위이며, 100입력 시, 100미만은 0, 100이상은 1로 디지털 입력 값이 반환되도록 합니다.
    """
    global triggerLevel
    triggerLevel = level


def _check_serial():
    return comm is not None and comm.is_open


def _make_buf(*args):
    length = len(args)
    buf = np.zeros(length + 3, dtype=np.uint8)
    buf[0] = 0x23
    buf[1] = len(args)
    buf[2:2 + len(args)] = args
    checksum = 0
    for arg in args:
        checksum ^= arg
    buf[-1] = checksum
    return buf


def _printf(message):
    global debug
    if debug:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"{current_time} - {message}")
