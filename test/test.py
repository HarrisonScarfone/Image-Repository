import subprocess
import json
import sys

def test_home_page():

    process = subprocess.Popen(
        ["curl", "-v", "-s", "app:8000"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        )

    stdout, stderr = process.communicate()

    print(process.returncode)

    # see if we get the home page html response from server
    if "<title>Image Repository</title>" in str(stdout):
        return True

    return False

def verify_good_return(input):
    if "200" in str(input):
        return True

def run_tests():

    tph = test_home_page()

    if not tph:
        raise Exception("Home page test failed")
    else:
        print("Home page up")

    tiu = verify_good_return(sys.argv[1])

    if not tiu:
        raise Exception("Image upload test failed")
    else:
        print("Image upload ok")

    tigk = verify_good_return(sys.argv[2])

    if not tigk:
        raise Exception("Image grab from keyword test failed")
    else:
        print("Image grab ok")

    tigfn = verify_good_return(sys.argv[3])

    if not tigfn:
        raise Exception("Image grab from filename test failed")

run_tests()