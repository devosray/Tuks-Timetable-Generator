from bs4 import BeautifulSoup
from tuks_timetable_generator import web_scraper, configuration

# Ensure that stored URL's still contain valid timetable data
def test_is_all_timetable_URLS_valid():
    soup = BeautifulSoup(web_scraper.download_url(configuration.HATFIELD_TIMETABLE_URL), 'html.parser')
    table_header_block = soup.find("thead")
    table_headers = table_header_block.find_all("th")
    valid_headers = [
        "Year / Module / Group / Lang / A No",
        "Type",
        "Day",
        "Start-Time",
        "End-Time",
        "Venue"
    ]
    for header in table_headers:
        string = header.string
        assert string in valid_headers