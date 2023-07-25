from classes.convert_filetemp_txt_to_dict import ConverterTxtToDict
from classes.read_file import ReaderTxt
from classes.save_inklinometer_data import SaveInlinometerData

path = 'data/data_port_spy_temp.txt'

reader_txt = ReaderTxt(path)

converter = ConverterTxtToDict()

data = converter.convert(reader_txt.read_all(encod='iso_8859_1'))

save_inklinometer1 = SaveInlinometerData('data/data_inklinometer_pp_temp.json', data)
save_inklinometer1.save_json()

print("Конвертация прошла успешно!")