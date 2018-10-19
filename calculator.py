import os
import csv
import sys


class Config:
    def __init__(self, configfile):
        self.configdata = {}
        self.configdata = self.readconfigfile(configfile)

    def readconfigfile(self, path):
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

    def readuserdatafile(self, path):
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


if __name__ == '__main__':
    cmdarg = Arg()
    shebaoData = Config(cmdarg.get_cfgfile())
    gzData = UserData(cmdarg.get_datafile())
    exportPath = cmdarg.get_exportfile()
    process_data = []
    shebaoTotalRatio = shebaoData.get_config('YangLao') + shebaoData.get_config('YiLiao') +\
        shebaoData.get_config('ShiYe') + shebaoData.get_config('GongShang') +\
        shebaoData.get_config('ShengYu') + shebaoData.get_config('GongJiJin')
    for onedata in gzData.userdata:
        income = onedata[1]
        shebaoHigh = shebaoData.get_config('JiShuH')
        shebaoLow = shebaoData.get_config('JiShuL')
        if income >= shebaoHigh:
            shebaoBase = shebaoHigh
        elif income <= shebaoLow:
            shebaoBase = shebaoLow
        else:
            shebaoBase = income
        shebaoje = shebaoBase*shebaoTotalRatio
        yincome = income-shebaoje-3500
        yintax = calculate_tax(yincome)
        postincome = income - shebaoje - yintax
        tuple_data = onedata[0], onedata[1], '{:.2f}'.format(shebaoje), '{:.2f}'.format(yintax), \
            '{:.2f}'.format(postincome)
        process_data.append(tuple_data)

    print(process_data)
    csvwriter = csv.writer(open(cmdarg.get_exportfile(), 'w'))
    csvwriter.writerows(process_data)

