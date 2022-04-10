from robot.api.deco import keyword
import json
from datetime import date
from selenium import *


class Tax:

    @keyword('natid validation')
    def natidvalidation(self,classlist):
        '''
        Created by : Amaresh Pathak
        Date : 19/03/2022
        This keyword is designed to validate natid value. All chars after 4 chars should be replaced
        with $
        '''
        flag = 'True'
        data = json.loads(classlist)
        for i in data:
            id = i['natid']
            if len(id) > 4:
                for l in range(5, len(id)+1):
                    if id[l-1:l:] != '$':
                        print('Fail {} - {}'.format(id[l-1:l:], l))
                        flag = 'False'
                    else:
                        print("Pass {} - {}".format(id[l-1:l:], l))
        return flag


    @keyword('calculate tax relief')
    def taxcalculation(self, classdata, classlist):
        '''
        Created by : Amaresh Pathak
        Date : 19/03/2022
        This keyword is designed to callulate the tax relief amount and validate the value from actual
        tax relief amount updated in database
        '''
        data = json.loads(classlist)
        for i in data:
            id = i['natid']
            if id[0:4:] == classdata['natid'][0:4:]:
                print('Pass - id = {} and classdata natid = {}'.format(id[0:4:], classdata['natid'][0:4:]))
                print(classdata)
                print(i)
                var = self.getagevariable(classdata['birthday'])
                bonus = self.getgenderbonus(classdata['gender'])

                # Tax Relief = ((salary - tax paid) * variable) + gender bonus
                print('Salary - {}, tax - {}, var - {}, Bonus - {}'.format(classdata['salary'],classdata['tax'], var, bonus))
                taxrelief = (float(classdata['salary']) - float(classdata['tax'])) * var + bonus
                x = str(taxrelief)[::-1].find('.')
                if x > 2:
                    length = len(str(taxrelief)) + 2 - x
                    taxrelief = float(str(taxrelief)[:length:])

                if taxrelief > 0.00 and taxrelief < 50.00:
                    taxrelief = 50.00

                taxrelief = round(taxrelief)
                print('taxrelief after calc = {}'.format(taxrelief))
                print('i[relief] - {},taxrelief - {}'.format(i['relief'], taxrelief))
                if round(float(i['relief'])) == taxrelief:
                    status = 'Pass'
                else:
                    status = 'Fail'

        return status



    def getagevariable(self,dob):
        '''
        Created by : Amaresh Pathak
        Date :
        This function is to find the age and variable value
        '''
        birthdate = date(int(dob[4:8:]), int(dob[2:4:]), int(dob[0:2:]))
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if age <= 18:
            var = 1
        elif age <= 35:
            var = .8
        elif age <= 50:
            var = .5
        elif age <= 75:
            var = .367
        elif age >= 76:
            var = .05
        return var

    def getgenderbonus(self, gender):
        '''
        Created by : Amaresh Pathak
        Date :
        This function is to find the gender bonus amount
        '''
        if gender == 'F':
            bonus = 500
        elif gender == 'M':
            bonus = 0
        return bonus

    @keyword('Open home page')
    def start(self, url):
        driver = webdriver.Chrome("C:\Assignment\chromedriver.exe")
        driver.get('http://localhost:8080/')


