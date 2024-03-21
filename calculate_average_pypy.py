import os, time

from collections import defaultdict
from multiprocessing import Pool, cpu_count


def get_file_chunks(file_name: str, cpu_count: int = 8) -> list:
    file_size = os.path.getsize(file_name)
    chunk_size = file_size // cpu_count
    chunk = list()
    with open(file_name, "r+b") as file:

        def is_new_line(position):
            if position == 0:
                return True
            else:
                file.seek(position - 1)
                return file.read(1) == b"\n"

        def next_line(position):
            file.seek(position)
            file.readline()
            return file.tell()

        chunk_start = 0
        while chunk_start < file_size:
            chunk_end = min(file_size, chunk_start + chunk_size)
            while not is_new_line(chunk_end):
                chunk_end -= 1
            if chunk_start == chunk_end:
                chunk_end = next_line(chunk_end)
            chunk.append(
                (
                    file_name,
                    chunk_start,
                    chunk_end,
                )
            )
            chunk_start = chunk_end
    return chunk


def process_chunk(chunk):
    file_name, chunk_start, chunk_end = chunk
    stations_temps = defaultdict(lambda: [float("inf"), float("-inf"), 0, 0])
    with open(file_name, "rb") as f:
        f.seek(chunk_start)
        buffersize = 2048 
        incomplete_line = b''
        while True:
            chunk = f.read(buffersize)
            chunk_start += buffersize
            if chunk_start > chunk_end:
                break
            lines = (incomplete_line + chunk).splitlines(True)
            incomplete_line = lines.pop() if lines[-1][-1:] != b'\n' else b''
            for line in lines:
                semicolon_pos = line.find(b';')
                temp = float(line[semicolon_pos + 1:].strip())
                station = stations_temps[line[:semicolon_pos].decode()]
                station[0] = min(temp, station[0])
                station[1] = max(temp, station[1])
                station[2] += temp
                station[3] += 1
                

    return dict(stations_temps)


def main(filename: str, cpu_count: int = cpu_count()):
    pool = Pool(cpu_count)

    chunks = get_file_chunks(filename, cpu_count)
    results = []
    for chunk in chunks:
        results.append(pool.apply_async(process_chunk, (chunk,)))
    pool.close()
    pool.join()

    stations_temps = dict()
    for result in results:
        chunk_result = result.get()
        for station in chunk_result.items():
            if stations_temps.get(station[0]) is None:
                stations_temps[station[0]] = station[1]
            else:
                if station[1][0] < stations_temps[station[0]][0]:
                    stations_temps[station[0]][0] = station[1][0]
                if station[1][1] > stations_temps[station[0]][1]:
                    stations_temps[station[0]][1] = station[1][1]
                stations_temps[station[0]][2] += station[1][2]
                stations_temps[station[0]][3] += station[1][3]

    answer = ", ".join(
        f"{station_name}={station[0]}/{station[2]/station[3]:.2f}/{station[1]}"
        for station_name, station in sorted(stations_temps.items())
    )

    print("{" + answer + "}")


if __name__ == "__main__":
    time_start = time.time()
    main("sample.txt", cpu_count())
    print(f"Elapsed time: {time.time()-time_start}")
