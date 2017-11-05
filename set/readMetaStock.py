"""
Little command line tool that covnerts Metastock 6.x data files
to text files with quotes.
"""

import sys, struct
import re
import traceback
import getopt
import os.path
import math

def xrange(x):
    return iter(range(x))

def fmsbin2ieee(bytes):
    """Convert an array of 4 bytes containing Microsoft Binary floating point
    number to IEEE floating point format (which is used by Python)"""
    as_int = struct.unpack("i", bytes)
    if not as_int:
        return 0.0
    man = int(struct.unpack('H', bytes[2:])[0])
    if not man:
        return 0.0
    exp = (man & 0xff00) - 0x0200
    #if (exp & 0x8000 != man & 0x8000):
        #raise ValueError('exponent overflow')
    man = man & 0x7f | (man << 8) & 0x8000
    man |= exp >> 1

    bytes2 = bytes[:2]
    bytes2 += chr(man & 255)
    bytes2 += chr((man >> 8) & 255)
    return struct.unpack("f", bytes2)[0]

def float2date(date):
    """Convert a float to a string containig a date"""
    date = int(date)
    year = 1900 + (date / 10000)
    month = (date % 10000) / 100
    day = date % 100
    return '%04d%02d%02d' % (year, month, day)

def float2time(time):
    """Convert a float to a string containig a time"""
    time = int(time)
    hour = time / 10000
    minute = (time % 10000) / 100
    return '%02d%02d' % (hour, minute)

class DataFileInfo(object):
    """
    Metastock data file
    """
    file_num = None
    num_fields = None
    stock_symbol = None
    reg = re.compile('\"(.+)\",.+', re.IGNORECASE)
    columns = None
    precision = 2

    def load_columns(self):
        """Read the columns from the DOP file"""
        filename = 'F%d.DAT' % self.file_num
        file_handle = open(filename, 'r')
        lines = file_handle.read().split()
        file_handle.close()
        assert(len(lines) == self.num_fields)
        self.columns = []
        for line in lines:
            match = self.reg.search(line)
            colname = match.groups()[0]
            self.columns.append(colname)

    unknownColumnDataSize = 4    # assume unknown column data is 4 bytes long

    class Column(object):
        """Base Metastock data file column class"""
        dataSize = 4

        def __init__(self, name, ms_name):
            self.name = name
            self.ms_name = ms_name

        def read(self, bytes):
            """Read and return a column value"""

    class DateColumn(Column):
        """A date column"""
        def read(self, bytes):
            """Convert from MBF to date string"""
            return float2date(fmsbin2ieee(bytes))

    class TimeColumn(Column):
        """A time column"""
        def read(self, bytes):
            """Convert read bytes from MBF to time string"""
            return float2time(fmsbin2ieee(bytes))

    class FloatColumn(Column):
        """A float column"""
        def read(self, bytes):
            """Convert bytes containing MBF to float"""
            return fmsbin2ieee(bytes)

    class IntColumn(Column):
        """An integer column"""
        def read(self, bytes):
            """Convert MBF bytes to an integer"""
            return int(fmsbin2ieee(bytes))

    knownColumns = [
        DateColumn('Date', 'DATE'),
        TimeColumn('Time', 'TIME'),
        FloatColumn('Open', 'OPEN'),
        FloatColumn('High', 'HIGH'),
        FloatColumn('Low', 'LOW'),
        FloatColumn('Close', 'CLOSE'),
        IntColumn('Volume', 'VOL'),
        IntColumn('Oi', 'OI'),
    ]

    max_recs = 0
    last_rec = 0

    def load_candles(self):
        """Load metastock DAT file and write the content
        to a text file"""
        file_handle = None
        outfile = None
        try:
            filename = 'F%d.DAT' % self.file_num
            file_handle = open(filename, 'rb')
            self.max_recs = struct.unpack("H", file_handle.read(2))[0]
            self.last_rec = struct.unpack("H", file_handle.read(2))[0]

            # not sure about this, but it seems to work
            file_handle.read((self.num_fields - 1) * 4)

            #print "Expecting %d candles in file %s. num_fields : %d" % \
            #    (self.last_rec - 1, filename, self.num_fields)

            outfile = open('%s.TXT' % self.stock_symbol, 'w')
            # write the header line, for example:
            #"Name","Date","Time","Open","High","Low","Close","Volume","Oi"
            outfile.write('"Name"')
            columns = []
            for ms_col_name in self.columns:
                column = None
                for _col in self.knownColumns:
                    if _col.ms_name == ms_col_name:
                        column = _col
                        outfile.write(',"%s"' % column.name)
                        break
                columns.append(column) # we append None if the columns is not known
            outfile.write('\n')

            # we have (self.last_rec - 1) candles to read
            for _ in xrange(self.last_rec - 1):
                outfile.write(self.stock_symbol)
                for col in columns:
                    if col is None:
                        file_handle.read(self.unknownColumnDataSize)
                    else:
                        bytes = file_handle.read(col.dataSize)
                        value = col.read(bytes)
                        if type(value) is float:
                            value = ("%0."+str(self.precision)+"f") % value
                        outfile.write(',%s' % value)

                outfile.write('\n')
        finally:
            if outfile is not None:
                outfile.close()
            if file_handle is not None:
                file_handle.close()

    def convert2ascii(self):
        """
        Load Metastock data file and output the data to text file.
        """
        print("Processing %s (fileNo %d)" % (self.stock_symbol, self.file_num))
        try:
            #print self.stock_symbol, self.file_num
            self.load_columns()
            #print self.columns
            self.load_candles()
        except Exception:
            print("Error while converting symbol", self.stock_symbol)
            traceback.print_exc()

class MSEMasterFile(object):
    """Metastock extended index file"""
    class _DataFileInfo(DataFileInfo):
        """
        Single index file entry
        """
        def __init__(self, file_handle):
            DataFileInfo.__init__(self)
            file_handle.read(2)
            self.file_num = struct.unpack("B", file_handle.read(1))[0]
            file_handle.read(3)
            self.num_fields = struct.unpack("B", file_handle.read(1))[0]
            #file_handle.read(4)
            #self.stock_symbol = file_handle.read(14).strip('\x00')
            #file_handle.read(7)
            #self.stock_name = file_handle.read(16).strip('\x00')
            file_handle.read(12)
            self.time_frame = struct.unpack("c", file_handle.read(1))[0]
            file_handle.read(3)
            self.first_date = float2date(struct.unpack("f", \
                                                       file_handle.read(4))[0])
            file_handle.read(4)
            self.last_date = float2date(struct.unpack("f", \
                                                      file_handle.read(4))[0])
            file_handle.read(116)

    stocks = None

    def __init__(self, filename):
        file_handle = open(filename, 'rb')
        self.files_no = struct.unpack("H", file_handle.read(2))[0]
        self.last_file = struct.unpack("H", file_handle.read(2))[0]
        file_handle.read(188)
        self.stocks = []
        #print self.files_no, self.last_file
        for _ in range(self.files_no):
            data = self._DataFileInfo(file_handle)
            self.stocks.append(data)
        file_handle.close()

    def list_all_symbols(self):
        """List all the symbols from metastock index file"""
        print("List of available symbols:")
        for stock in self.stocks:
            #print("symbol: %s, name: %s, file number: %s" % \
            #    (stock.stock_symbol, stock.stock_name, stock.file_num))
            print("symbol: %s, file number: %s" % \
                (stock.stock_symbol, stock.file_num))

    def output_ascii(self, all_symbols, symbols):
        """Read all or specified symbols and output them to text
        files"""
        for stock in self.stocks:
            if all_symbols or (stock.stock_symbol in symbols):
                stock.convert2ascii()

def print_usage():
    """Print help screen"""
    name = os.path.basename(sys.argv[0])
    print("Usage:\n%s [--help | --list | --all | -p precision] [symbol1] [symbol2] ...." % name)
    print("Examples:")
    print("%s --list            list all the symbols from EMASTER file" % name)
    print("%s --all             extract all the symbols from EMASTER file" % name)
    print("%s -p 4              round the floating point values to 4 digits after the decimal point" % name)
    print("%s FW20 \"S&P500\"   extract FW20 and S&P500 from EMASTER file" % name)

if __name__ == "__main__":
    try:
        OPTLIST, SYMBOLS = getopt.getopt(sys.argv[1:], 'p:',
                                         ['list', 'all', 'help'])
    except Exception:
        print("Error:" + Exception)
        print_usage()
        sys.exit(0)
    OPTLIST = dict(OPTLIST)
    if "--help" in OPTLIST:
        print_usage()
        sys.exit(0)
    if "-p" in OPTLIST:
        try:
            p = int(OPTLIST["-p"])
        except:
            p = -1
        if p < 0 or p > 32:
            print("Invalid presicion supplied: " + OPTLIST["-p"])
            print_usage()
            sys.exit(0)
        DataFileInfo.precision = p
    EM = MSEMasterFile('C:\Set\EMASTER')
    if "--list" in OPTLIST:
        EM.list_all_symbols()
        sys.exit(0)

    ALL_SYMBOLS = "--all" in OPTLIST
    if (not ALL_SYMBOLS) and (len(SYMBOLS) == 0):
        print_usage()
        sys.exit(0)

    EM.output_ascii(ALL_SYMBOLS, SYMBOLS)