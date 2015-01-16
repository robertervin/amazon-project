from django.core.management.base import BaseCommand
from mws import mws
import traceback
from amazon_api.settings import SECRET_KEY, AWS_ACCESS_KEY_ID, MWS_AUTH_TOKEN, SELLER_ID

class Command(BaseCommand):
    help = "Run ./manage.py test_feed_submission_result <feed_submission_id>"
    
    def handle(self, *args, **options):
        feed_submission_id = args[0]
        
        req = mws.Feeds(
            access_key=AWS_ACCESS_KEY_ID, 
            secret_key=SECRET_KEY,
            account_id=SELLER_ID,
            region="US"
            )
        try:
            res = req.get_feed_submission_result(
                feedid=feed_submission_id
                )
            print res.__dict__
        except:
            traceback.print_exc()
