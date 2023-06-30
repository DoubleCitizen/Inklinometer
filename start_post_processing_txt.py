from classes.read_file import ReaderTxt
from classes.convert_file_txt_to_dict3 import ConverterTxtToDict
from classes.save_inklinometer_data import SaveInlinometerData

path = 'data/data_port_spy_2.txt'

reader_txt = ReaderTxt(path)

converter = ConverterTxtToDict()

data: dict = converter.convert(reader_txt.read_all())

save_inklinometer1 = SaveInlinometerData('data/data_inklinometer_pp_nivel.json', data)
save_inklinometer1.save_json()

print("Конвертация прошла успешно!")


