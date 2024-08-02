import os, time, mmap

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


def get_subchunks(start: int, end: int, file_name: str, devide_by: int) -> list:
    chunk = list()
    chunk_size = (end - start) // devide_by
    with open(file_name, "rb") as file:

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

        chunk_start = start
        while chunk_start < end:
            chunk_end = min(end, chunk_start + chunk_size)
            while not is_new_line(chunk_end):
                chunk_end -= 1
            if chunk_start == chunk_end:
                chunk_end = next_line(chunk_end)
            chunk.append(chunk_end - chunk_start)
            chunk_start = chunk_end
    return chunk


def process_chunk(chunk) -> dict:
    file_name, chunk_start, chunk_end = chunk
    length = chunk_end - chunk_start
    new_chunk_start = chunk_start - (chunk_start % mmap.ALLOCATIONGRANULARITY)
    diff = chunk_start - new_chunk_start
    stations_temps = defaultdict(lambda: [100, -100, 0, 0])
    with open(file_name, "rb") as f:
        with mmap.mmap(
            f.fileno(),
            length=length + diff,
            offset=new_chunk_start,
            access=mmap.ACCESS_READ,
        ) as mm:
            mm.madvise(mmap.MADV_SEQUENTIAL)
            mm.seek(diff)
            subchunks = get_subchunks(chunk_start, chunk_end, file_name, 20)
            
            for subchunk in subchunks:
                buffer = mm.read(subchunk)
                index = 0
                while index < subchunk:
                    semicolon = buffer.find(b";", index)
                    newline = buffer.find(b"\n", semicolon)

                    temp = float(buffer[semicolon + 1: newline].strip())
                    station_vals = stations_temps[buffer[index:semicolon]]
                    if temp < station_vals[0]:
                        station_vals[0] = temp
                    if temp > station_vals[1]:
                        station_vals[1] = temp
                    station_vals[2] += temp
                    station_vals[3] += 1
                    index = newline + 1

                
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
        for station_name, station_vals in chunk_result.items():
            station = stations_temps.get(station_name)
            if station:
                station[0] = min(station[0], station_vals[0])
                station[1] = max(station[1], station_vals[1])
                station[2] += station_vals[2]
                station[3] += station_vals[3]
            else:
                stations_temps[station_name] = station_vals

    answer = ", ".join(
        f"{station_name.decode()}={station[0]}/{station[2]/station[3]:.2f}/{station[1]}"
        for station_name, station in sorted(stations_temps.items())
    )

    print("{" + answer + "}")


if __name__ == "__main__":
    time_start = time.time()
    main("sample.txt", 16)
    print(f"Elapsed time: {time.time() - time_start}")
