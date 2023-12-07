class Stats:
    """Отслеживание статистики"""

    def __init__(self):
        """Инициализация статистики"""
        self.reset_stat()
        self.continuing_game = True
        self.level = 1
        with open('txt_files/record.txt', 'r') as file:
            self.record = int(file.readline())

    def reset_stat(self):
        """Отслеживание статистики"""
        self.guns_left = 3
        self.value_score = 0
        self.level = 1

    def level_up(self):
        self.level += 1
