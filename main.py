"""
Уровень 1. Файл log_100.json:
1) чему равен общий вклад топ-3 всех IP по количеству посещений? Указать процентом
2) сколько в файле уникальных IP, с которых на сайт заходили только 1 раз

Уровень 2. Файл log_cereals.csv:
3) наименьшая стоимость пачки манки
4) средняя цена на крупу за весь период наблюдений

Уровень 3. Файл log_full.csv:
5) найти максимально часто встречающийся IP
6) посчитать в процентах вклад этого IP адреса в общее кол-во запросов
7) найти последнюю запись в логах с этим IP и выяснить какой user-agent был у этой записи
получить словарь:
suspicious_agent = {
    "ip": '...',            # самый частовстречаемый ip в логах
    'fraction': 70.205,     # процент запросов с таким ip от общего кол-ва запросов
    'count': 29427,         # число запросов с таким IP
    'last': {               # вложенный словарь с 2-мя полями
        'agent': '...',     # последний user-agent для этого ip
        'timestamp': '...', # последний timestap для этого ip
    }
}
"""
import csv
import json


#region Level 3.
def start_level3():
    path: str = './log_full.csv'
    ips: list = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == 'ip':
                continue
            ips.append(row[1])

    unique_ips: list = list(set(ips))
    print(len(unique_ips))

    ip_indexes: list = []
    for ip in unique_ips:
        ip_indexes.append(ips.count(ip))

    max_used_ip: dict = {
      "index": ip_indexes.index(max(ip_indexes)),
      "value": unique_ips[ip_indexes.index(max(ip_indexes))],
      "times": max(ip_indexes)
    }

    max_used_ip["fraction"] = (max_used_ip['times']/len(ips)) * 100
    print(f"Max used IP is {unique_ips[max_used_ip['index']]} with {max_used_ip['times']} times")
    print(f"Total filling of IP {unique_ips[max_used_ip['index']]} is {max_used_ip['fraction']}%")

    full_log: list = []
    log_row: list = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            full_log.append(row)
    for row in full_log[::-1]:
      if max_used_ip['value'] in row:
          log_row.append(row)
          break

    log_row = list(list(log_row))
    print("\n")

    suspicious_agent: dict = {
      "ip": max_used_ip["value"],
      "fraction": max_used_ip["fraction"],
      "count": max_used_ip["times"],
      "last": {
          "user-agent": log_row[0][2],
          "timestamp": log_row[0][0],
      }
    }

    with open('agent_dump.json', 'w') as f:
        json.dump(suspicious_agent, f, indent=4)
#endregion


#region Level 2.
def start_level2() -> None:
    path: str = './log_cereals.csv'
    first_prices: list = []
    second_prices: list = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
              first_prices.append(float(row[1]))
              second_prices.append(float(row[2]))
            except:
               continue
    print(first_prices)
    print(second_prices)

    min = first_prices[0]
    for i in first_prices:
       if i < min:
          min = i
    print(f'The least first price is {min}')

    sum: int = 0
    for i in range(0, len(first_prices) - 1):
       sum += first_prices[i] + second_prices[i]

    result = sum / len(first_prices) * 2
    print(f"Average price for the all time is {result}")
#endregion


#region Level 1.
def start_level1() -> None:
    path = './log_100.json'
    with open(path, 'r') as f:
        lst: list = json.load(f)
    print(len(lst))

    ips = {
      "ip0": "207.46.13.17",
      "ip1": "46.229.168.142",
      "ip2": "54.36.148.131",
      "ip3": "185.180.12.65",
      "ip4": "195.38.23.97",
      "ip5": "66.249.79.252",
      "ip6": "188.138.40.20",
      "ip7": "105.103.189.78",
      "ip8": "5.140.82.74",
      "ip9": "66.165.233.234",
      "ip10": "156.172.24.24",
      "ip11": "5.178.78.77",
      "ip12": "46.229.168.130",
      "ip13": "23.101.169.3",
      "ip14": "207.46.13.18",
      "ip15": "79.136.245.135",
      "ip16": "213.87.104.248"
    }
    counts: list = []

    for k,v in ips.items():
      count = 0
      for i in lst:
        if v in i["ip"]:
          count += 1
      counts.append(count)

    print(counts)
    print(f"Total filling of top-3 IPs is {round((counts[13] + counts[15] + counts[16])/len(lst) * 100)}%")

    for i in range(0, len(counts)-1):
       if counts[i] <= 1:
          print(ips[f"ip{i}"])
#endregion

def main():
    # Uncomment for starting specify level.
    # start_level1()
    # start_level2()
    start_level3()


if __name__ == '__main__':
    main()