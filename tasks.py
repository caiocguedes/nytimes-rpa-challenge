from robocorp.tasks import task
from robocorp import browser
from rpa_data_extractor import RPADataExtractorApp

@task
def rpaDataExtractor():
    app = RPADataExtractorApp()
    app.run()
    
    
