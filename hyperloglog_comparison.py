import time
import json
import hyperloglog

def load_ip_addresses(file_path):
  ip_addresses = []
  try:
    with open(file_path, "r") as file:
      for line in file:
        try:
          data = json.loads(line.strip())
          ip = data.get("remote_addr")
          if ip:
            ip_addresses.append(ip)
        except json.JSONDecodeError:
          continue
  except FileNotFoundError:
    print(f"File '{file_path}' not found.")
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
    print("No valid IP addresses found.")
  else:
    exact_count, exact_time = exact_unique_count(ip_addresses)

    approx_count, approx_time = approximate_unique_count(ip_addresses)

    print("Результати порівняння:")
    print(f"{'':<25}{'Точний підрахунок':<20}{'HyperLogLog':<20}")
    print(f"{'Унікальні елементи':<25}{exact_count:<20}{approx_count:<20}")
    print(f"{'Час виконання (сек.)':<25}{exact_time:<20.5f}{approx_time:<20.5f}")