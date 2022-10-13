

import os
from dotenv import load_dotenv
load_dotenv()
def main():
   os.system(os.getenv("service"))
if __name__ == "__main__":
    main()
    
    