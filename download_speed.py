import argparse
from http.client import HTTPException, HTTPResponse
from time import perf_counter
from urllib.request import urlopen


REQUEST_COUNT = 10


def download(url: str) -> int:
    with urlopen(url, timeout=30) as response:
        size = sum(len(chunk) for chunk in iter(lambda: response.read(65536), b""))
        if isinstance(response, HTTPResponse) and response.length:
            raise OSError(f"неполный ответ, не хватает {response.length} байт")
        return size


def main() -> None:
    parser = argparse.ArgumentParser(description="Замер скорости скачивания")
    parser.add_argument("url", help="HTTP(S)-адрес файла")
    url = parser.parse_args().url
    if not url.lower().startswith(("http://", "https://")):
        parser.error("укажи адрес, начинающийся с http:// или https://")

    total_bytes = 0
    total_time = 0.0
    for number in range(1, REQUEST_COUNT + 1):
        started = perf_counter()
        try:
            total_bytes += download(url)
        except (OSError, HTTPException, ValueError) as error:
            parser.exit(1, f"Запрос {number}/{REQUEST_COUNT}: {error}\n")
        total_time += perf_counter() - started

    print(f"Среднее время запроса: {total_time / REQUEST_COUNT:.3f} с")
    print(f"Скачано: {total_bytes} байт")
    print(f"Скорость скачивания: {total_bytes * 8 / total_time / 1_000_000:.2f} Мбит/с")


if __name__ == "__main__":
    main()
