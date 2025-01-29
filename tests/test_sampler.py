#####################################################################################
#
# Author: Murtaza Mushtaq
# Unit tests for air_quality_sampler
#
#####################################################################################

import unittest
from air_quality_sampler import AirQualitySampler
from unittest.mock import patch, MagicMock

class TestAirQualitySampler(unittest.TestCase):

    def test_start_stop_sampling(self):
        sampler = AirQualitySampler()
        sampler.start_sampling(lat1=40.0, lon1=-74.0, lat2=41.0, lon2=-73.0, sampling_period=1, sampling_rate=1)
        sampler.stop_sampling()
        status, _ = sampler.get_status()
        self.assertEqual(status, "STOPPED")

    @patch("air_quality_sampler.requests.get")
    def test_fetch_pm25_data_success(self, mock_get):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "data": [
                {"pm25": {"v": 10.0}},
                {"pm25": {"v": 20.0}},
                {"pm25": {"v": 30.0}},
            ],
        }
        mock_get.return_value = mock_response
        avg_pm25 = self.sampler._fetch_pm25_data(lat1=40.0, lon1=-74.0, lat2=41.0, lon2=-73.0)
        self.assertEqual(avg_pm25, 20.0)  # (10 + 20 + 30) / 3 = 20

    @patch("air_quality_sampler.requests.get")
    def test_fetch_pm25_data_no_data(self, mock_get):
        # Mock API response with no PM2.5 data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "data": [
                {"no2": {"v": 5.0}},  # No PM2.5 data
            ],
        }
        mock_get.return_value = mock_response
        avg_pm25 = self.sampler._fetch_pm25_data(lat1=40.0, lon1=-74.0, lat2=41.0, lon2=-73.0)
        self.assertIsNone(avg_pm25)

    @patch("air_quality_sampler.requests.get")
    def test_fetch_pm25_data_api_error(self, mock_get):
        # Mock API error response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "error",
            "data": "Invalid token",
        }
        mock_get.return_value = mock_response
        avg_pm25 = self.sampler._fetch_pm25_data(lat1=40.0, lon1=-74.0, lat2=41.0, lon2=-73.0)
        self.assertIsNone(avg_pm25)

    @patch("air_quality_sampler.requests.get")
    def test_fetch_pm25_data_request_exception(self, mock_get):
        # Mock request exception
        mock_get.side_effect = requests.RequestException("Network error")
        avg_pm25 = self.sampler._fetch_pm25_data(lat1=40.0, lon1=-74.0, lat2=41.0, lon2=-73.0)
        self.assertIsNone(avg_pm25)

    def test_start_sampling_already_running(self):
        self.sampler.sampling_status = "RUNNING"
        self.sampler.start_sampling(lat1=40.0, lon1=-74.0, lat2=41.0, lon2=-73.0, sampling_period=1, sampling_rate=1)
        self.assertEqual(self.sampler.sampling_status, "RUNNING")  # Status should remain unchanged

    def test_stop_sampling_not_running(self):
        self.sampler.sampling_status = "IDLE"
        self.sampler.stop_sampling()
        self.assertEqual(self.sampler.sampling_status, "IDLE")  # Status should remain unchanged

    @patch("air_quality_sampler.requests.get")
    def test_sampling_completes_successfully(self, mock_get):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "data": [
                {"pm25": {"v": 10.0}},
                {"pm25": {"v": 20.0}},
                {"pm25": {"v": 30.0}},
            ],
        }
        mock_get.return_value = mock_response
        self.sampler.start_sampling(lat1=40.0, lon1=-74.0, lat2=41.0, lon2=-73.0, sampling_period=1, sampling_rate=1)
        time.sleep(2)  # Wait for sampling to complete
        status, avg_pm25 = self.sampler.get_status()
        self.assertEqual(status, "DONE")
        self.assertEqual(avg_pm25, 20.0)  # (10 + 20 + 30) / 3 = 20

    @patch("air_quality_sampler.requests.get")
    def test_sampling_fails_no_data(self, mock_get):
        # Mock API response with no PM2.5 data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "data": [
                {"no2": {"v": 5.0}},  # No PM2.5 data
            ],
        }
        mock_get.return_value = mock_response
        self.sampler.start_sampling(lat1=40.0, lon1=-74.0, lat2=41.0, lon2=-73.0, sampling_period=1, sampling_rate=1)
        time.sleep(2)  # Wait for sampling to complete
        status, avg_pm25 = self.sampler.get_status()
        self.assertEqual(status, "FAILED")
        self.assertIsNone(avg_pm25)

if __name__ == "__main__":
    unittest.main()
