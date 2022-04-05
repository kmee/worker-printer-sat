import logging
import io
import base64
from satextrato import config
from satextrato import ExtratoCFeVenda, ExtratoCFeCancelamento

_logger = logging.getLogger(__name__)


def imprimir_extrato(xml, tipo_impressora, impressora, parametros_impressora, xml_cancelamento):
    try:
        print_config = config.carregar('/odoo/sat/satextrato.ini')
    except Exception as e:
        print_config = config.padrao()

    if tipo_impressora == 'NetworkConnection':
        from escpos.conn.network import NetworkConnection as Connection
        conn = Connection(host=parametros_impressora, port=9100)
    elif tipo_impressora == 'BluetoothConnection':
        from escpos.conn.bt import BluetoothConnection as Connection
    elif tipo_impressora == 'DummyConnection':
        from escpos.conn.dummy import DummyConnection as Connection
        conn = Connection()
    elif tipo_impressora == 'FileConnection':
        from escpos.conn.file import FileConnection as Connection
        conn = Connection(parametros_impressora)
    elif tipo_impressora == 'SerialConnection':
        from escpos.conn.serial import SerialSettings as Connection
        conn = Connection.parse(parametros_impressora).get_connection()
    elif tipo_impressora == 'USBConnection':
        from escpos.conn.usb import USBConnection as Connection
        conn = Connection(interface=parametros_impressora)

    if impressora == 'epson-tm-t20':
        _logger.info('SAT Impressao: Epson TM-T20')
        from escpos.impl.epson import TMT20 as Printer
    elif impressora == 'bematech-mp4200th':
        _logger.info('SAT Impressao: Bematech MP4200TH')
        from escpos.impl.bematech import MP4200TH as Printer
    elif impressora == 'daruma-dr700':
        _logger.info('SAT Impressao: Daruma Dr700')
        from escpos.impl.daruma import DR700 as Printer
    elif impressora == 'elgin-i9':
        _logger.info('SAT Impressao: Elgin I9')
        from escpos.impl.elgin import ElginI9 as Printer
    else:
        return False

    printer = Printer(conn)

    from escpos import feature
    printer.hardware_features.update({
        feature.COLUMNS: feature.Columns(
            normal=42,
            expanded=24,
            condensed=56)
    })
    printer.init()

    if not xml_cancelamento:
        ExtratoCFeVenda(
            fp=io.StringIO(base64.b64decode(xml).decode('utf-8')),
            impressora=printer, config=print_config
        ).imprimir()
    else:
        ExtratoCFeCancelamento(
            io.StringIO(base64.b64decode(xml).decode('utf-8')),
            io.StringIO(base64.b64decode(xml_cancelamento).decode('utf-8')),
            printer
        ).imprimir()
