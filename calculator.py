import os
import csv
import sys
from multiprocessing import Process, Queue
import getopt
import configparser
from datetime import  datetime


class Config:
    def __init__(self, configfile):
        self.configdata = self.readconfigfile(configfile)

    @staticmethod
    def readconfigfile(path):
        configparas = {}
        if not os.path.isfile(path):
            print('{} not exists'.format(path))
            return configparas
        else:
            with open(path, 'r') as f:
                for line in f.readlines():
                    arg_list = line.split('=')
                    try:
                        configparas[arg_list[0].strip()] = float(arg_list[1].strip())
                    except NameError:
                        print('configfile read fail')
                        return configparas
            return configparas

    def get_config(self, key):
        return self.configdata[key]


class UserData:
    def __init__(self, csv_file):
        self.userdata = self.readuserdatafile(csv_file)

    @staticmethod
    def readuserdatafile(path):
        data = []
        if not os.path.isfile(path):
            print('{} not exists'.format(path))
            return data
        else:
            with open(path, 'r') as f:
                for line in csv.reader(f):
                    try:
                        gongzi = int(line[1].strip())
                    except NameError:
                        print('configfile read fail')
                        return data
                    data.append((line[0], gongzi))
            return data


class Arg:
    def __init__(self):
        self.args = sys.argv[1:]

    def get_cfgfile(self):
        index = self.args.index('-c')
        return self.args[index+1]

    def get_datafile(self):
        index = self.args.index('-d')
        return self.args[index + 1]

    def get_exportfile(self):
        index = self.args.index('-o')
        return self.args[index + 1]


def calculate_tax(value):
    if value <= 0:
        tax = 0
    elif value <= 1500:
        tax = value * 0.03
    elif value <= 4500:
        tax = value * 0.10 - 105
    elif value <= 9000:
        tax = value * 0.20 - 555
    elif value <= 35000:
        tax = value * 0.25 - 1005
    elif value <= 55000:
        tax = value * 0.30 - 2755
    elif value <= 80000:
        tax = value * 0.35 - 5505
    else:
        tax = value * 0.40 - 13505
    return tax


def readdata(q1, v_userdatapath):
    # print('this is process 1 for read user id and income, process id {}'.format(os.getpid()))
    gzdata = UserData(v_userdatapath)
    q1.put(gzdata)


def processdata(q1, q2, v_configfilepath, v_cityname):
    # print('this is process 2 for calculate user income data, process id {}'.format(os.getpid()))
    gzdata = q1.get()  # get user id and income data from queue1
    process_data = []

    # get shebao data from configfile
    cnf = configparser.ConfigParser()
    cnf.read(v_configfilepath)
    cityname = v_cityname.upper()  # city name ignore case

    shebaototalratio = cnf.getfloat(cityname, 'YangLao') + cnf.getfloat(cityname, 'YiLiao') +\
        cnf.getfloat(cityname, 'ShiYe') + cnf.getfloat(cityname, 'GongShang') +\
        cnf.getfloat(cityname, 'ShengYu') + cnf.getfloat(cityname, 'GongJiJin')
    shebaohigh = cnf.getfloat(cityname, 'JiShuH')
    shebaolow = cnf.getfloat(cityname, 'JiShuL')

    for onedata in gzdata.userdata:
        income = onedata[1]
        if income >= shebaohigh:
            shebaobase = shebaohigh
        elif income <= shebaolow:
            shebaobase = shebaolow
        else:
            shebaobase = income
        shebaoje = shebaobase * shebaototalratio
        yincome = income - shebaoje - 3500
        yintax = calculate_tax(yincome)
        postincome = income - shebaoje - yintax
        tuple_data = onedata[0], onedata[1], '{:.2f}'.format(shebaoje), '{:.2f}'.format(yintax), '{:.2f}'.format(
            postincome), datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        process_data.append(tuple_data)
    q2.put(process_data)  # put the calculated data on queue2


def exportdata(q2, v_gzexportpath):
    # print('this is process 3 for export calculated data to csv file, process id {}'.format(os.getpid()))
    processdataq2 = q2.get()
    csvexport = csv.writer(open(v_gzexportpath, 'w'))
    csvexport.writerows(processdataq2)


def usage():
    print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hC:c:d:o:", ["help"])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)
    cityname = 'DEFAULT'
    for option, optvalue in opts:
        if option in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif option == "-C":
            cityname = optvalue
        elif option == "-c":
            configfilepath = optvalue
        elif option == "-d":
            userdatapath = optvalue
        elif option == "-o":
            gzexportpath = optvalue
        else:
            assert False, "Unhandled option"

    # cmdarg = Arg()
    queue1 = Queue()  # store user id and income data
    queue2 = Queue()  # store calculated data
    Process(target=readdata, args=(queue1, userdatapath)).start()
    Process(target=processdata, args=(queue1, queue2, configfilepath, cityname)).start()
    Process(target=exportdata, args=(queue2, gzexportpath)).start()


if __name__ == '__main__':
    #print('this is main process for auxliary, process id {}'.format(os.getpid()))
    main()
