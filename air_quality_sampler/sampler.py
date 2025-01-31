
#####################################################################################
#
# Author: Murtaza Mushtaq
# Module to sample and calculate average PM2.5 levels within a specified map bound
#
#####################################################################################

import logging
import time
import requests
from typing import Optional, Tuple
from threading import Thread, Event

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class AirQualitySampler:
    def __init__(self):
        self.sampling_status = "IDLE"
        self.avg_pm25_all_sites = None
        self._stop_event = Event()
        self._thread = None

    def _fetch_pm25_data(self, lat1: float, lon1: float, lat2: float, lon2: float) -> Optional[float]:
        # Fetch PM2.5 data for all stations within the map bound
        url = "https://api.waqi.info/map/bounds/"
        params = {
            "latlng": f"{lat1},{lon1},{lat2},{lon2}",
            "token": "0b078f2ecf07cd80eca5dcee52bd8a67af08b66a" # my private api token downloaded from the website
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["status"] != "ok":
                logger.error(f"API error: {data.get('data', 'Unknown error')}")
                return None

            pm25_values = [station["pm25"]["v"] for station in data["data"] if "pm25" in station]
            if not pm25_values:
                logger.warning("No PM2.5 data found for the given bounds.")
                return None

            return sum(pm25_values) / len(pm25_values)
        except requests.RequestException as e:
            logger.error(f"Failed to fetch data: {e}")
            return None

    def _sample(self, lat1: float, lon1: float, lat2: float, lon2: float, sampling_period: int, sampling_rate: int):
        # Perform sampling over the specified period
        samples = []
        interval = 60 / sampling_rate  # Interval between samples in seconds
        total_samples = sampling_period * sampling_rate

        for _ in range(total_samples):
            if self._stop_event.is_set():
                self.sampling_status = "STOPPED"
                logger.info("Sampling stopped by user.")
                return

            pm25_avg = self._fetch_pm25_data(lat1, lon1, lat2, lon2)
            if pm25_avg is not None:
                samples.append(pm25_avg)

            time.sleep(interval)

        if samples:
            self.avg_pm25_all_sites = sum(samples) / len(samples)
            self.sampling_status = "DONE"
        else:
            self.sampling_status = "FAILED"
            logger.error("No valid PM2.5 samples collected.")

    def start_sampling(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        sampling_period: int = 5,
        sampling_rate: int = 1
    ):
        # Start sampling PM2.5 data
        if self.sampling_status == "RUNNING":
            logger.warning("Sampling is already running.")
            return

        self.sampling_status = "RUNNING"
        self.avg_pm25_all_sites = None
        self._stop_event.clear()
        self._thread = Thread(
            target=self._sample,
            args=(lat1, lon1, lat2, lon2, sampling_period, sampling_rate)
        )
        self._thread.start()
        logger.info("Sampling started.")

    def stop_sampling(self):
        # Stop sampling
        if self.sampling_status == "RUNNING":
            self._stop_event.set()
            self._thread.join()
            logger.info("Sampling stopped.")
        else:
            logger.warning("No active sampling to stop.")

    def get_status(self) -> Tuple[str, Optional[float]]:
        # Get the current sampling status and average PM2.5
        return self.sampling_status, self.avg_pm25_all_sites