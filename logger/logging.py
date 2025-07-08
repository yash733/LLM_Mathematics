import logging
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='./logger/.log',
                    filemode='w')