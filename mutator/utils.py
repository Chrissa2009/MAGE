import time
import csv

def write_time(domain, url, mutation_times, total_time, csv_writer):
    """
    Writes timing results to a CSV file.
    
    Parameters:
    - domain: The domain name of the URL
    - url: The full URL
    - mutation_times: dict with keys 'distractor', 'shuffle', 'original' and values in seconds
    - total_time: float, total elapsed time for the URL
    - csv_writer: an open CSV writer object
    """
    csv_writer.writerow([
        domain,
        url,
        f"{total_time:.2f}",
        f"{mutation_times.get('distractor', 0):.2f}",
        f"{mutation_times.get('shuffle', 0):.2f}",
        f"{mutation_times.get('original', 0):.2f}"
    ])