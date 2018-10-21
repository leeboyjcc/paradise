import os
import csv
import sys
from multiprocessing import Process, Queue


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


def readdata(q1, v_cmdarg):
    print('this is process 1 for read user id and income, process id {}'.format(os.getpid()))
    gzdata = UserData(v_cmdarg.get_datafile())
    q1.put(gzdata)


def processdata(q1, q2, v_cmdarg):
    print('this is process 2 for calculate user income data, process id {}'.format(os.getpid()))
    gzdata = q1.get()
    shebaodata = Config(v_cmdarg.get_cfgfile())
    process_data = []
    shebaototalratio = shebaodata.get_config('YangLao') + shebaodata.get_config('YiLiao') + \
        shebaodata.get_config('ShiYe') + shebaodata.get_config('GongShang') + \
        shebaodata.get_config('ShengYu') + shebaodata.get_config('GongJiJin')
    for onedata in gzdata.userdata:
        income = onedata[1]
        shebaohigh = shebaodata.get_config('JiShuH')
        shebaolow = shebaodata.get_config('JiShuL')
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
            postincome)
        process_data.append(tuple_data)
    q2.put(process_data)


def exportdata(q2, v_cmdarg):
    print('this is process 3 for export calculated data to csv file, process id {}'.format(os.getpid()))
    processdataq2 = q2.get()
    exportpath = v_cmdarg.get_exportfile()
    csvexport = csv.writer(open(exportpath, 'w'))
    csvexport.writerows(processdataq2)


def main():
    cmdarg = Arg()
    queue1 = Queue()  # store user id and income data
    queue2 = Queue()  # store calculated data
    Process(target=readdata, args=(queue1, cmdarg)).start()
    Process(target=processdata, args=(queue1, queue2, cmdarg)).start()
    Process(target=exportdata, args=(queue2, cmdarg)).start()


if __name__ == '__main__':
    print('this is main process for auxliary, process id {}'.format(os.getpid()))
    main()
