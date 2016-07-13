from tuks_timetable_generator import web_scraper, configuration

print("Downloading and parsing latest timetable...")
module_list = web_scraper.download_and_parse_url(configuration.HATFIELD_TIMETABLE_URL)

print("Finished parsing timetable")
