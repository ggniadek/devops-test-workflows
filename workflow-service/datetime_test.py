# Test for folder creation in lambda and S3
from datetime import datetime
import math

def test():
     date_time = datetime.now().timestamp()
     print(math.floor(date_time))
     
test()