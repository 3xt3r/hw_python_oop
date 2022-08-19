from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = (
        'Тип тренировки: {training_type}; Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        try:
            return self.message.format(**asdict(self))
        except (KeyError, IndexError):
            raise NotImplementedError(
                'Ошибка при обращении к словарю данных с датчиков'
            )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч"""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories в классах-наследниках'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег.
    Расчет в get_spent_calories() в следующих единицах:
    длительность тренировки (duration): минуты
    cредняя скорость (mean_speed): км/ч"""
    COEFF_1: int = 18
    COEFF_2: int = 20

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        calories = (self.COEFF_1 * mean_speed - self.COEFF_2) * self.weight
        return calories / self.M_IN_KM * self.duration * self.MIN_IN_HOUR


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    Расчет в get_spent_calories() в следующих единицах:
    длительность тренировки (duration): минуты
    cредняя скорость (mean_speed): км/ч"""
    COEFF_1: float = 0.035
    COEFF_2: float = 0.029
    COEFF_3: int = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        result = self.COEFF_1 * self.weight
        + mean_speed**self.COEFF_3 // self.height * self.COEFF_2 * self.weight
        return result * self.duration * self.MIN_IN_HOUR


class Swimming(Training):
    """Тренировка: плавание.
    Расчет в get_spent_calories() в следующих единицах:
    длительность тренировки (duration): часы
    cредняя скорость (mean_speed): км/ч
    длина бассейна (length_pool): метры """
    LEN_STEP: float = 1.38
    COEFF_1: float = 1.1
    COEFF_2: int = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool,
                 count_pool
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        total_distance = self.length_pool * self.count_pool
        return total_distance / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return (mean_speed + self.COEFF_1) * self.COEFF_2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_training: Dict[str, List[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return type_of_training[workout_type](*data)
    except (KeyError, IndexError):
        raise NotImplementedError(
            'Попытка обращения к несуществующему типу тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
