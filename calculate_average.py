import time
from collections import defaultdict


class Station:
    def __init__(self, temp):
        self.min_temp = temp
        self.max_temp = temp
        self.sum_temp = temp
        self.count = 1

    def add_temp(self, temp):
        self.min_temp = min(self.min_temp, temp)
        self.max_temp = max(self.max_temp, temp)
        self.sum_temp += temp
        self.count += 1

    def average_temp(self):
        return self.sum_temp / self.count


stations_temps = defaultdict(Station)


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"Elapsed time: {end-start}")

    return wrapper


def read_large_file(file_object):
    """A generator to read a large file lazily."""
    while True:
        data = file_object.readline()
        if not data:
            break
        yield data


@timing_decorator
def main():
    with open("sample.txt", "r") as file:
        gen = read_large_file(file)
        for line in gen:
            station_name, temp = line.split(";")
            temp = float(temp)
            station = stations_temps.get(station_name)
            if station:
                station.add_temp(temp)
            else:
                stations_temps[station_name] = Station(temp)

    answer = ", ".join(
        f"{station}={temps.min_temp}/{temps.average_temp()}/{temps.max_temp}"
        for station, temps in sorted(stations_temps.items())
    )

    print("{" + answer + "}")


if __name__ == "__main__":
    main()
