import time
from collections import defaultdict

stations_temps = defaultdict(lambda: [float('inf'), float('-inf'), 0, 0])


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
    with open("sample.txt", "rb") as file:
        gen = read_large_file(file)
        for line in gen:
            station_name, temp = line.split(b";")
            temp = float(temp)
            station = stations_temps[station_name]
            station[0] = min(station[0], temp)
            station[1] = max(station[1], temp)
            station[2] += temp
            station[3] += 1

    answer = ", ".join(
        f"{station_name.decode()}={station[0]}/{station[2]/station[3]:.2f}/{station[1]}"
        for station_name, station in sorted(stations_temps.items())
    )

    print("{" + answer + "}")


if __name__ == "__main__":
    main()
