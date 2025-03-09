import hashlib
from bitarray import bitarray

class BloomFilter:
    """Реалізація фільтра Блума для перевірки унікальності паролів."""
    
    def __init__(self, size=1000, num_hashes=3):
        """
        Ініціалізація фільтра Блума.
        :param size: Розмір бітового масиву.
        :param num_hashes: Кількість хеш-функцій.
        """
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)  # Ініціалізуємо всі біти як 0

    def _hashes(self, item):
        """Генерує num_hashes хешів для елемента."""
        hashes = []
        for i in range(self.num_hashes):
            hash_value = int(hashlib.md5(f"{item}{i}".encode()).hexdigest(), 16) % self.size
            hashes.append(hash_value)
        return hashes

    def add(self, item):
        """Додає елемент у фільтр Блума."""
        for index in self._hashes(item):
            self.bit_array[index] = 1

    def check(self, item):
        """Перевіряє, чи був елемент у фільтрі Блума."""
        return all(self.bit_array[index] for index in self._hashes(item))

def check_password_uniqueness(bloom_filter, passwords):
    """
    Перевіряє список паролів на унікальність за допомогою фільтра Блума.
    :param bloom_filter: Екземпляр BloomFilter.
    :param passwords: Список паролів для перевірки.
    :return: Словник з результатами перевірки.
    """
    if not isinstance(passwords, list) or not all(isinstance(p, str) for p in passwords):
        raise ValueError("Помилка: Вхідні дані повинні бути списком рядків")

    results = {}
    for password in passwords:
        if bloom_filter.check(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)  # Додаємо унікальний пароль у фільтр
    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")