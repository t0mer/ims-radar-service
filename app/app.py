import time
import json
import schedule
import requests
from loguru import logger
from radar_satellite import RadarSatellite

radar_url = "https://ims.gov.il/he/radar_satellite"
images_url = "https://ims.gov.il"
weather2day_base_url = "https://www.weather2day.co.il/images/radar/"
weather2day_images_url = "https://www.weather2day.co.il/radar-last.txt"
rs = RadarSatellite()


def _fetch_data(url: str) -> dict:
    """
    Helper method to get the Json data from ims website
    """
    try:
        response = requests.get(url)
        response = json.loads(response.text)
        return response
    except Exception as e:
        logger.error('Error getting data. ' + str(e))
        logger.exception(e)
        return dict()

def _fetch_data_weather2day(url: str) -> str:
    """
    Helper method to get the Json data from ims website
    """
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        logger.error('Error getting data. ' + str(e))
        logger.exception(e)
        return ""



def get_radar_images():
    '''
    Get the list of images for Satellite and Radar
    return: RadarSatellite objects with the lists
    '''
    
    try:
        logger.debug('Getting radar images')
        data = _fetch_data(radar_url)
   
        weather2day_images = _fetch_data_weather2day(weather2day_images_url).strip().split('\n')[:22]
        for image in reversed(weather2day_images):
            rs.radar_images.append(weather2day_base_url + image)

        for key in data.get("data").get("types").get("MIDDLE-EAST"):
            rs.middle_east_satellite_images.append(images_url + key.get("file_name"))

        for key in data.get("data").get("types").get("EUROPE"):
            rs.europe_satellite_images.append(images_url + key.get("file_name"))

        rs.generate_images()

        logger.debug(f"\
            Got: {len(rs.radar_images)} Radar Images;\
            {len(rs.middle_east_satellite_images)} Middle East Satellite Images;\
            {len(rs.europe_satellite_images)} European Satellite Images")
        rs.radar_images.clear()
        rs.middle_east_satellite_images.clear()
        rs.europe_satellite_images.clear()
        return rs
    except Exception as e:
        logger.error('Error getting images. ' + str(e))
        rs.radar_images.clear()
        rs.middle_east_satellite_images.clear()
        rs.europe_satellite_images.clear()
        return rs
    
if __name__=="__main__":
    get_radar_images()
    schedule.every(1).minutes.do(get_radar_images)
    while True:
        schedule.run_pending()
        time.sleep(1)