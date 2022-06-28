from application import create_app
from config import DevelopmentConfig, ProductionConfig, TestingConfig
import logging
from application.utils.first_request import create_dev_db, create_prod_db


dev_app = create_app(DevelopmentConfig)
prod_app = create_app(ProductionConfig)
test_app = create_app(TestingConfig)

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


dev_app.before_first_request(create_dev_db)
test_app.before_first_request(create_dev_db)
prod_app.before_first_request(create_prod_db)
