import time
import json
import re
import hyperloglog

def load_ip_addresses(file_path):
    ip_addresses = []
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)')
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    # Якщо лог у форматі JSON
                    data = json.loads(line.strip())
                    ip = data.get("remote_addr")
                except json.JSONDecodeError:
                    # Якщо лог у звичайному текстовому форматі
                    match = pattern.search(line)
                    ip = match.group(1) if match else None
                
                if ip:
                    ip_addresses.append(ip)
    except FileNotFoundError:
        print(f"❌ Файл '{file_path}' не знайдено.")
    
    return ip_addresses

def exact_unique_count(ip_addresses):
    start_time = time.time()
    unique_ips = set(ip_addresses)
    duration = time.time() - start_time
    return len(unique_ips), duration

def approximate_unique_count(ip_addresses):
    start_time = time.time()
    hll = hyperloglog.HyperLogLog(0.01)
    for ip in ip_addresses:
        hll.add(ip)
    count = len(hll)
    duration = time.time() - start_time
    return count, duration

if __name__ == "__main__":
    log_file_path = "lms-stage-access.log"

    ip_addresses = load_ip_addresses(log_file_path)

    if not ip_addresses:
        print("❌ Не знайдено жодної IP-адреси у файлі.")
    else:
        print(f"📌 Загальна кількість рядків у логах: {len(ip_addresses)}")
        print(f"📌 Унікальних IP перед підрахунком: {len(set(ip_addresses))}")

        exact_count, exact_time = exact_unique_count(ip_addresses)

        approx_count, approx_time = approximate_unique_count(ip_addresses)

        print("\n📊 Результати порівняння:")
        print(f"{'':<25}{'Точний підрахунок':<20}{'HyperLogLog':<20}")
        print(f"{'Унікальні елементи':<25}{exact_count:<20}{approx_count:<20}")
        print(f"{'Час виконання (сек.)':<25}{exact_time:<20.5f}{approx_time:<20.5f}")