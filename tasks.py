from robocorp.tasks import task
from robocorp import browser
from main import RPADataExtractorApp

@task
def rpaDataExtractor():
    app = RPADataExtractorApp()
    app.run()
    
    
