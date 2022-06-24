import random

def get_roll(array: list) -> int:
    """
    Функция для получения спина
    :param array: Предыдущие спины, исходя
    из которых мы получим новый спин
    :return int: Новый спин
    """

    available_rolls = [ roll for roll in range(1, 11) if roll not in array ]

    if not available_rolls:
        return 11

    # получаем рандомный спин
    roll = random.choice(available_rolls)

    return roll