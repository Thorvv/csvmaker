# coding=utf-8

import pandas as pd
import numpy as np
import re
import csv

PATH = u"./"
MOBILE = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')


class Manager(object):
    def __init__(self, excel_name):
        self.path_name = PATH + excel_name
        if excel_name[-3:] == 'csv':
            self.df = pd.read_csv(self.path_name, sep=None, encoding="gbk")
        else:
            self.df = pd.read_excel(self.path_name, sheetname=0)


def paser_phone(phone):
    new_phone = phone.strip()
    if phone == 'nan':
        return ''
    if phone[0:3] == '+86':
        new_phone = phone[3:]
        if new_phone[0] != '1':
            new_phone = phone[4:]
    return new_phone


def paser_data(csv_1, total_count):
    user_dict_1 = {}
    user_dict_2 = {}
    for row in range(0, total_count):
        user_name = csv_1.df["Given Name"][row]
        phone_1 = paser_phone(str(csv_1.df["Phone 1 - Value"][row]).strip())
        phone_2 = paser_phone(str(csv_1.df["Phone 2 - Value"][row]).strip())
        """
        if phone_1 != '' and phone_2 != '':
            user_dict[user_name] = phone_1 + '|' + phone_2
        elif phone_2 == '':
            user_dict[user_name] = phone_1
        else:
            user_dict[user_name] = phone_2
        """
        user_dict_1[user_name] = phone_1
        user_dict_2[user_name] = phone_2
    return user_dict_1, user_dict_2


def paser_call_list(csv_2):
    final_col = ''
    check_csv = csv_2.df.head()
    for col in check_csv.columns:
        for flag in check_csv[col]:
            try:
                phone_match = MOBILE.match(flag.encode("utf-8"))
            except:
                phone_match = MOBILE.match(str(flag))
            if phone_match:
                final_col = col
                break
    return list(csv_2.df[final_col])


def count_times(user_dict, call_list):
    count_list = []
    for keys in user_dict:
        count_list.append(call_list.count(user_dict[keys]))
    return count_list


def excel_maker(countlist, namelist, mobilelist):
    count_size = len(countlist)
    csvfile = file('./csvtest.csv', 'wb')
    # writer = csv.writer(csvfile)
    writer = csv.writer(open("test.csv", 'wb'))
    writer.writerow(['name', 'mobile', 'times'])
    for row in range(count_size):
        print namelist[row], countlist[row], mobilelist[row]
        writer.writerows([namelist[row], countlist[row], mobilelist[row]])
    csvfile.close()


if __name__ == "__main__":
    csv_1 = Manager(u"2017-02-23-12-11-55-contact-5.csv")
    total_count = len(csv_1.df)
    user_dict_1, user_dict_2 = paser_data(csv_1, total_count)

    csv_2 = Manager(u"2017年01月语音通信.xls")
    call_list = []
    tmp_list = paser_call_list(csv_2)
    for call in tmp_list:
        call_list.append(paser_phone(str(call)))

    l1 = count_times(user_dict_1, call_list)
    l2 = count_times(user_dict_2, call_list)
    countlist = map(lambda (a, b): a+b, zip(l1, l2))
    namelist = user_dict_1.keys()
    mobilelist = []
    for key in user_dict_1:
        mobilelist.append(user_dict_1[key])
    excel_maker(countlist, namelist, mobilelist)

