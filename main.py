import concurrent.futures
import time
from functools import partial
from base_modules.utils import gen_date_intervals
from base_modules.voluum_api import extract_conversions_data, fetch_columns
from base_modules.config import credentials


if __name__ == "__main__":
    # Example of Multi-Threading Data Extraction
    t1 = time.perf_counter()
    backfill_dates = gen_date_intervals('2020-04-18', '2020-04-27', inv_size=2)
    p_extract_voluum_conversions = partial(extract_conversions_data,
                                           fetch_cols=fetch_columns,
                                           credentials=credentials,
                                           filter_by_col='campaignName',
                                           predicate='Google Ads')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(p_extract_voluum_conversions, backfill_dates)

    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')

    # Example of Multi-Processing Data Extraction
    t1 = time.perf_counter()
    backfill_dates = gen_date_intervals('2020-03-01', '2020-04-01', inv_size=31)
    p_extract_voluum_conversions = partial(extract_conversions_data,
                                           fetch_cols=fetch_columns,
                                           credentials=credentials,
                                           filter_by_col='campaignName',
                                           predicate='Google Ads')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(p_extract_voluum_conversions, backfill_dates)

    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')
