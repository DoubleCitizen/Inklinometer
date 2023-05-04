from classes.read_file import ReaderTxt
from classes.convert_file_txt_to_dict import ConverterTxtToDict

path = 'data/data_port_spy_3.txt'

reader_txt = ReaderTxt(path)

converter = ConverterTxtToDict()

print(reader_txt.read_all())
