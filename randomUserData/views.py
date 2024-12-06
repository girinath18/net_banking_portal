import os
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
import numpy as np
import pandas as pd

try:
    import seaborn as sbn
    import matplotlib.pyplot as plt
    print("Successfully imported seaborn and matplotlib")
except ImportError as e:
    print("ImportError:", e)

class Random(TemplateView):
    def __init__(self):
        # Define file paths relative to the project base directory
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.branch_file = os.path.join(self.base_dir, r'V:\net_banking_portal\random-branches.csv')
        self.address_file = os.path.join(self.base_dir, r'V:\net_banking_portal\addresses.csv')

    def getRandomBranch(self):
        try:
            branch = pd.read_csv(self.branch_file, delimiter=',').to_numpy()
            randomBranch = branch[np.random.randint(len(branch))]
            ret = str(randomBranch)
            return ret[2:len(ret) - 2]
        except Exception as e:
            return f"Error reading branch data: {e}"

    def getRandomMobileNumber(self):
        num = "+3816" + str(np.random.randint(0, 9)) + str(np.random.randint(1000, 9999)) + str(np.random.randint(100, 9999))
        return num

    def getRandomAddress(self):
        try:
            address = pd.read_csv(self.address_file, delimiter=',').to_numpy()
            randomAddress = address[np.random.randint(len(address))]
            ret = str(randomAddress)
            return ret[2:len(ret) - 2]
        except Exception as e:
            return f"Error reading address data: {e}"

    def getRandomHouseNumber(self):
        return str(np.random.randint(1, 100))

def index(request):
    return HttpResponse("Success")

def getRandomData(request):
    random = Random()  # Instantiate the Random class
    bra = random.getRandomBranch()
    adr = random.getRandomAddress()
    num = random.getRandomMobileNumber()
    hnum = random.getRandomHouseNumber()
    return JsonResponse({'number': num, 'address': adr, 'hnumber': hnum, 'branch': bra})
