from parsing import URLS2, parse_and_save
from time import time

def main():
    for i in range(len(URLS2)):
        parse_and_save(URLS2[i])
    
    

if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print("Time: " + str(end - start))