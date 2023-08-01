import fnmatch
import os

from classes.read_file import ReaderTxt
from classes.convert_file_txt_to_dict_notaver import ConverterTxtToDict
from classes.convert_file_txtmp4_to_dict import ConverterTxtToDict as Converter_mp4txt
from classes.save_inklinometer_data import SaveInlinometerData
from classes.convert_filetemp_txt_to_dict import ConverterTxtToDict as Converter_temptxt


# Обработка Nivel 220
path = 'data/data_port_spy_2.txt'
reader_txt = ReaderTxt(path)
converter = ConverterTxtToDict()
data: dict = converter.convert(reader_txt.read_all())

save_nivel = SaveInlinometerData('data/data_inklinometer_pp_nivel.json', data)
save_nivel.save_json()

# Обработка температурного датчика
path = 'data/data_port_spy_temp.txt'
reader_txt = ReaderTxt(path)
converter = Converter_temptxt()
data: dict = converter.convert(reader_txt.read_all(encod='iso_8859_1'))

save_temperature_detector = SaveInlinometerData('data/data_inklinometer_pp_temp.json', data)
save_temperature_detector.save_json()


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


list_txt_processing = find('*.mp4.txt', 'data')
new_list_txt = []
for json in list_txt_processing:
    new_txt = json.split('\\')[1]
    new_list_txt.append(new_txt)

for id, txt_file in enumerate(new_list_txt):
    reader_txt = ReaderTxt(f'data/{txt_file}')
    converter = Converter_mp4txt()
    data = converter.convert(reader_txt.read_all())
    save_inklinometer = SaveInlinometerData(f'data/{txt_file}.json', data)
    save_inklinometer.save_json()
    print(f'Файл {txt_file} обработан {(id+1 / len(new_list_txt)) * 100}%')


print("Конвертация прошла успешно!")
