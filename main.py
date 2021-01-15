import zipfile


class Analyze:
    analyze_count = 1

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat = {}

    def unzip(self):
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for filename in zfile.namelist():
            zfile.extract(filename)
            self.file_name = filename

    def collect(self):
        if self.file_name.endswith('.zip'):
            self.unzip()
        self.sequence = ' ' * self.analyze_count
        with open(self.file_name, 'r', encoding='cp1251') as file:
            for line in file:
                self._collect_for_line(line=line[:-1])  # [:-1] это нужно для обрезки "\n" в конце строки

    def _collect_for_line(self, line):
        for char in line:
            if char.isalpha():
                if char in self.stat:
                    self.stat[char] += 1
                else:
                    self.stat[char] = 1


class AnalyzeText(Analyze):
    def __init__(self, file_name):
        super().__init__(file_name=file_name)

    def out_stat(self, first_column_width, second_column_width, type, revers: bool):
        self.first_column_width = first_column_width
        self.second_column_width = second_column_width
        self.type = type
        self.revers = revers

        print(f'+{"":-^{self.first_column_width}}' + f'+{"":-^{self.second_column_width}}+')
        print(f'|{"буква":^{self.first_column_width}}' + f'|{"частота":^{self.second_column_width}}|')
        print(f'+{"":-^{self.first_column_width}}' + f'+{"":-^{self.second_column_width}}+')

        if self.type == 1:
            self.sort_by_alphabet()
        elif self.type == 2:
            self.sort_by_values()

        print(f'+{"":-^{self.first_column_width}}' + f'+{"":-^{self.second_column_width}}+')
        print(f'|{"итого":^{self.first_column_width}}' + f'|{sum(self.stat.values()):^{self.second_column_width}}|')
        print(f'+{"":-^{self.first_column_width}}' + f'+{"":-^{self.second_column_width}}+')

    def sort_by_alphabet(self):
        for char in sorted(self.stat.keys(), reverse=self.revers):
            print(f'|{char:^{self.first_column_width}}' + f'|{self.stat[char]:^{self.second_column_width}}|')

    def sort_by_values(self):
        for char, value in sorted(self.stat.items(), reverse=self.revers, key=lambda item: item[1]):
            print(f'|{char:^{self.first_column_width}}' + f'|{value:^{self.second_column_width}}|')


def start():
    text = str(input('Введите название ".txt" или ".zip" файла вместе с расширением: '))
    analyze_text = AnalyzeText(text)
    analyze_text.collect()
    print('Файл обработан.\nНастройте таблицу:')
    first_column = int(input('Ширина первой колонки(5 - 20): '))
    second_column = int(input('Ширина второй колонки(9 - 30): '))

    print('Выберите сортировку:\n'
          '1. По алфавиту\n'
          '2. По алфавиту, в обратном порядке\n'
          '3. По частоте использования буквы, по возрастанию\n'
          '4. По частоте использования буквы, по убыванию\n'
          '5. Выход из программы\n')

    while True:
        choise = int(input('Введите число от 1 до 5: '))
        if choise == 1:
            analyze_text.out_stat(first_column, second_column, type=1, revers=False)
            break
        elif choise == 2:
            analyze_text.out_stat(first_column, second_column, type=1, revers=True)
            break
        elif choise == 3:
            analyze_text.out_stat(first_column, second_column, type=2, revers=False)
            break
        elif choise == 4:
            analyze_text.out_stat(first_column, second_column, type=2, revers=True)
            break
        elif choise == 5:
            break
        else:
            print('Введена не корректная команда. Повторите попытку.')


if __name__ == '__main__':
    start()
