import classterizer   

class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Processing(metaclass=MetaSingleton):
    def __init__(self):
        self.report = None

    def set_report(self, report):
        self.report = report

    def get_cluster(self):
        return self.report


class Model(object):  # todo SINGLETON class

    @staticmethod
    def send_report(report):#наш текст 
        dict = {0: 'регестрация', 1: 'происходить', 2: 'зайти', 3: 'личный кабинет', 4: 'мусор', 5: 'получаться', 6: 'пароль', 7: 'сайт',
        8: 'проблемы с поиском', 9: 'проблемы с телефоном', 10: 'проблемы с заполнением заявления', 11: 'мусор', 12: 'проблемы с ответом', 
        13: 'что-то не загружается ', 14: 'проблемы с паролем/письмом', 15: 'мусор', 16: 'возникновение ошибки/проблемы', 17: 'проблемы с выходом', 18: 'проблемы с отправкой', 19: 'проблемы с компьютером/программой/сайтом/системой'}

        predict_class = classterizer.load_predict(report)
        # print("Введенное сообщение относится к классу, который можно охарактеризовать следующими словами  =  "+dict[predict_class[0]])  # todo initialization SINGLETON if python can
        Processing().set_report("Введенное сообщение относится к классу, который можно охарактеризовать следующими словами  =  "+dict[predict_class[0]])

    @staticmethod
    def get_response():
        return "Отчёт принят!\n{}".format(Processing().get_cluster())
