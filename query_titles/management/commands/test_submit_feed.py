from products.models import Product
from scripts.webstore import Publish

from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = "Run ./manage.py test_submit_feed"

    def handle(self, *args, **options):
        products = Product.objects.all()[:5]
        publish = Publish(products)
        res = publish.run()
        print res

        # SAMPLE REQUEST
        # <?xml version="1.0" encoding="UTF-8" ?>
        #     <root>
                # <item type="dict">
                #     <Product type="dict">
                #         <StandardProductID type="dict">
                #             <Type type="str">ASIN</Type>
                #             <Value type="str">B00HSMQYU8</Value>
                #         </StandardProductID>
                #     </Product>
                # </item>
        #         <item type="dict">
        #             <Product type="dict">
        #                 <StandardProductID type="dict">
        #                     <Type type="str">ASIN</Type>
        #                     <Value type="str">B00A3KZAVG</Value>
        #                 </StandardProductID>
        #             </Product>
        #         </item>
        #     </root>


        # SAMPLE RESPONSE
        # {  
        #    'response':<Response   [  
        #       200
        #    ]   >,
        #    '_rootkey':'SubmitFeedResult',
        #    'original':'<?xml version="1.0"?>\n<SubmitFeedResponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/"><SubmitFeedResult><FeedSubmissionInfo><FeedSubmissionId>50007016441</FeedSubmissionId><FeedType>_POST_PRODUCT_DATA_</FeedType><SubmittedDate>2015-01-06T17:55:21+00:00</SubmittedDate><FeedProcessingStatus>_SUBMITTED_</FeedProcessingStatus></FeedSubmissionInfo></SubmitFeedResult><ResponseMetadata><RequestId>bd9e233a-1fe3-4de9-ac2b-a2526362f8d5</RequestId></ResponseMetadata></SubmitFeedResponse>',
        #    '_mydict':{  
        #       'SubmitFeedResponse':{  
        #          'ResponseMetadata':{  
        #             'RequestId':{  
        #                'value':'bd9e233a-1fe3-4de9-ac2b-a2526362f8d5'
        #             }
        #          },
        #          'SubmitFeedResult':{  
        #             'FeedSubmissionInfo':{  
        #                'FeedProcessingStatus':{  
        #                   'value':'_SUBMITTED_'
        #                },
        #                'FeedType':{  
        #                   'value':'_POST_PRODUCT_DATA_'
        #                },
        #                'SubmittedDate':{  
        #                   'value':'2015-01-06T17:55:21+00:00'
        #                },
        #                'FeedSubmissionId':{  
        #                   'value':'50007016441'
        #                }
        #             }
        #          }
        #       }
        #    },
        #    '_response_dict':{  
        #       'ResponseMetadata':{  
        #          'RequestId':{  
        #             'value':'bd9e233a-1fe3-4de9-ac2b-a2526362f8d5'
        #          }
        #       },
        #       'SubmitFeedResult':{  
        #          'FeedSubmissionInfo':{  
        #             'FeedProcessingStatus':{  
        #                'value':'_SUBMITTED_'
        #             },
        #             'FeedType':{  
        #                'value':'_POST_PRODUCT_DATA_'
        #             },
        #             'SubmittedDate':{  
        #                'value':'2015-01-06T17:55:21+00:00'
        #             },
        #             'FeedSubmissionId':{  
        #                'value':'50007016441'
        #             }
        #          }
        #       }
        #    }
        # }