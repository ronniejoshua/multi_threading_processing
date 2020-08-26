#!/usr/bin/env python3
""" Challenge: Download a collection of images """

import time
import urllib.request
import multiprocessing as mp
import concurrent.futures


def seq_download_images(image_numbers):
    """ sequential implementation of multiple image downloader
        returns total bytes from downloading all images in image_numbers list """
    total_bytes = 0
    for num in image_numbers:
        total_bytes += _download_image(num)
    return total_bytes


def _download_image(image_number):
    """ helper function returns number of bytes from downloading image """
    # force between 1 and 50
    image_number = (abs(image_number) % 50) + 1
    image_url = f"http://699340.youcanlearnit.net/image{image_number:03d}.jpg"
    try:
        with urllib.request.urlopen(image_url, timeout=60) as conn:
            # number of bytes in downloaded image
            return len(conn.read())
    except urllib.error.HTTPError:
        print('HTTPError: Could not retrieve image ', image_number)
    except Exception as e:
        print(e)


def par_download_images(image_numbers):
    """ parallel implementation of multiple image downloader
        returns total bytes from downloading all images in image_numbers list """
    total_bytes = 0
    with concurrent.futures.ThreadPoolExecutor() as pool:
        futures = [pool.submit(_download_image, num) for num in image_numbers]
        for f in concurrent.futures.as_completed(futures):
            total_bytes += f.result()
    return total_bytes


if __name__ == '__main__':
    NUM_EVAL_RUNS = 1
    IMAGE_NUMBERS = list(range(1, 50))

    print('Evaluating Sequential Implementation...')
    sequential_result = seq_download_images(IMAGE_NUMBERS)
    sequential_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        seq_download_images(IMAGE_NUMBERS)
        sequential_time += time.perf_counter() - start
    sequential_time /= NUM_EVAL_RUNS

    print('Evaluating Parallel Implementation...')
    parallel_result = par_download_images(IMAGE_NUMBERS)
    parallel_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        par_download_images(IMAGE_NUMBERS)
        parallel_time += time.perf_counter() - start
    parallel_time /= NUM_EVAL_RUNS

    if sequential_result != parallel_result:
        raise Exception('sequential_result and parallel_result do not match.')
    print('Average Sequential Time: {:.2f} ms'.format(sequential_time * 1000))
    print('Average Parallel Time: {:.2f} ms'.format(parallel_time * 1000))
    print('Speedup: {:.2f}'.format(sequential_time / parallel_time))
    print('Efficiency: {:.2f}%'.format(100 * (sequential_time / parallel_time) / mp.cpu_count()))
