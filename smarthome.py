
import csv
import copy
from datetime import datetime
import numpy as np
from numpy import matrix
import ghmm
from ghmm import *

### check the correctness of start/end times of detections in path_file.txt
### and generate the relative path_file.csv file
def check_and_generate_csv(path_file):
    print 'check file >> %s.txt <<' %path_file
    file_input = open(path_file+'.txt').readlines()
    ### to count lines in file
    for i, l in enumerate(file_input):
        pass
    tot_detection = i-1

    list_detection = []
    error = False
    iter_detection = iter(file_input)
    try:
        ### two times next() to jump first and second line in file (header of tables)
        next(iter_detection)
        next(iter_detection)
        next_line = next(iter_detection)
        init_error = False
    except StopIteration:
        init_error = True
    if not init_error:
        for c in range(tot_detection):
            smart_line = []
            this_line = next_line.split('\t')
            for col in this_line:
                if col and not col.isspace():
                    col = col.strip()
                    smart_line.append(col)
            start = datetime.strptime(smart_line[0], '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(smart_line[1], '%Y-%m-%d %H:%M:%S')
            try:
                next_line = next(iter_detection)
                next_empty = False
            except StopIteration:
                next_empty = True
            if start <= end:
                # if not next_empty:
                #     ### check: this_line.end and next_line.start
                #     next_smart_line = []
                #     nxt_line = next_line.split('\t')
                #     for co in nxt_line:
                #         if co and not co.isspace():
                #             co = co.strip()
                #             next_smart_line.append(co)
                #     next_start = datetime.strptime(next_smart_line[0], '%Y-%m-%d %H:%M:%S')
                #     if end <= next_start:
                #         list_detection.append(smart_line)
                #     else:
                #         error = True
                #         print '\tstart/end time mismatch in lines %s and %s\n\t%s\n\t%s' %(counter+3, counter+4, smart_line, next_smart_line)
                #
                #     ### check correctness between start and start in next row
                #     next_smart_line = []
                #     nxt_line = next_line.split('\t')
                #     for co in nxt_line:
                #         if co and not co.isspace():
                #             co = co.strip()
                #             next_smart_line.append(co)
                #     next_start = datetime.strptime(next_smart_line[0], '%Y-%m-%d %H:%M:%S')
                #     if start <= next_start:
                #         list_detection.append(smart_line)
                #     else:
                #         error = True
                #         print '\tstart/end time mismatch in lines %s and %s\n\t%s\n\t%s' %(counter+3, counter+4, smart_line, next_smart_line)

                list_detection.append(smart_line) #comment if used above controls
            else:
                error = True
                print '\tstart/end time mismatch at line %s\n\t %s' %(c+3, smart_line)

    if not error:
        with open(path_file +'.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', delimiter='\t')
            for line in list_detection:
                writer.writerow(line)
        print '\tcorrectly loaded in >> %s.csv <<\n' %path_file
        del list_detection, iter_detection
    else:
        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print '[!] there are errors in file:'
        print '[!] \t>> %s.txt <<' % path_file
        print '[!] please fix them before continuing.'
        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
        del list_detection, iter_detection
        quit()

### normalize list structure
def normalize_list(list):
    tot = 0
    for elem in list:
        tot += elem
    part = 0
    for c, elem in enumerate(list):
        if c+1 == len(list):
            list[c] = 1.00 - part
        else:
            list[c] = np.divide(float(list[c]), float(tot))
            part += list[c]

### print matrix structure
def print_matrix(matrix):
    for line in matrix:
        print line

### normalize matrix structure
def normalize_matrix(matrix):
    for row in matrix:
        normalize_list(row)

    # for x, row in enumerate(matrix):
    #     tot_in_row = 0
    #     for col in row:
    #         tot_in_row += col
    #     if tot_in_row != 0:
    #         part_in_row = 0
    #         for y, col in enumerate(row):
    #             if y+1 == len(row):
    #                 matrix[x][y] = round(1.00 - part_in_row, 9)
    #             else:
    #                 matrix[x][y] = round(np.divide(float(matrix[x][y]), float(tot_in_row)), 9)
    #                 part_in_row += matrix[x][y]

### create csv from lists
def csv_list(list_names, list_values, file_name):
    if (len(list_names) != len(list_values)):
        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print '[!] error in method'
        print '[!] csv_list(list_names, list_values, file_name)'
        print '[!] \t-> len(list_names) != len(list_values)'
        print '[!] please fix before continuing.'
        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
        quit()
    else:
        with open(file_name +'.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', delimiter='\t')
            first_line = []
            for x in list_names:
                first_line.append(x)
            writer.writerow(first_line)
            new_line = []
            for y in list_values:
                new_line.append(y)
            writer.writerow(new_line)
        print '\tloaded in >> %s.csv <<' %file_name

### create csv from matrix
def csv_matrix(list_rows, list_columns, matrix, file_name):
    with open(file_name +'.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', delimiter='\t')
        first_line = ['\t']
        for x in list_columns:
            first_line.append(x)
        writer.writerow(first_line)
        new_line = []
        for c, y in enumerate(list_rows):
            new_line.append(y)
            for z in range(len(matrix)):
                new_line.append(matrix[c][z])
            writer.writerow(new_line)
            new_line = []
    print '\tloaded in >> %s.csv <<' %file_name

### obtain probability of each adl
### return [list_adls] = list of adls and [p_adls]= list of their probability
### p(y) = p(adl)
def obtain_p_adls(path_file, house_name):
    tot_rows = len(open(path_file+'.csv').readlines())
    list_adls = []
    p_adls = []
    with open(path_file+'.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, dialect='excel', delimiter='\t')
        for row in reader:
            adl = copy.deepcopy(row[2])
            exist_adl = False
            for c, a in enumerate(list_adls):
                if (a == adl):
                    p_adls[c] += 1
                    exist_adl = True
            if not exist_adl:
                list_adls.append(adl)
                p_adls.append(1)
        normalize_list(p_adls)
    print '%s: P(ADLs) calculated' %house_name
    csv_list(list_adls, p_adls, house_name+'_P(ADLs)')
    return list_adls, p_adls

### obtain probability of transition between adls
### return [t_adls] = [matrix] = matrix with transition probabilities
### p(y(t)|y(t-1)) = p(adl(t)|adl(t-1))
def obtain_t_adls(path_file, list_adls, house_name):
    ### initialize square matrix of transition between adls
    matrix = []
    for a in list_adls:
        l = []
        for b in list_adls:
            l.append(0)
        matrix.append(l)
    tot_rows = len(open(path_file+'.csv').readlines())
    with open(path_file+'.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, dialect='excel', delimiter='\t')
        iter_file = iter(reader)
        next_row = next(iter_file)
        for i in range(tot_rows):
            this_a = next_row[2]
            try:
                next_row = next(iter_file)
                next_empty = False
            except StopIteration:
                next_empty = True
            if not next_empty:
                next_a = next_row[2]
                for x, a in enumerate(list_adls):
                    if a == this_a:
                        for y, b in enumerate(list_adls):
                            if b == next_a:
                                matrix[x][y] += 1
    normalize_matrix(matrix)
    print '%s : T(ADLs) calculated' %house_name
    csv_matrix(list_adls, list_adls, matrix, house_name+'_T(ADLs)')
    return matrix

def obtain_list_sens(path_file, house_name):
    ### build list of all possible triple Location-Type-Place
    ### ad save the order of sensors detections
    list_sens = []
    # sens_seq = ''
    sens_seq = []
    with open(path_file+'.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, dialect='excel', delimiter='\t')
        for row in reader:
            sens = '%s %s %s' %(copy.deepcopy(row[2]), copy.deepcopy(row[3]), copy.deepcopy(row[4]))
            exist_sens = False
            for c, s in enumerate(list_sens):
                if s == sens:
                    exist_sens = True
                    # sens_seq += '%s' %c
                    sens_seq.append(c)
            if not exist_sens:
                list_sens.append(sens)
                # sens_seq += '%s' %(len(list_sens)-1)
                sens_seq.append(len(list_sens)-1)
    return list_sens, sens_seq

### obtain probability of observations sens from adls
### return [o_sens_adls] = [matrix] = matrix with observations probabilities
### p(x|y) = p(sens|adls)
def obtain_o_sens_adls(path_adls, list_adls, path_sens, list_sens, house_name):
    ### initialize matrix of observation 
    matrix = []
    for a in list_adls:
        l = []
        for s in list_sens:
            l.append(0)
        matrix.append(l)

    with open(path_adls+'.csv', 'rb') as csv_adls:
        reader_adls = csv.reader(csv_adls, dialect='excel', delimiter='\t')
        for a in reader_adls:
            adl = a[2]
            start_a = datetime.strptime(a[0], '%Y-%m-%d %H:%M:%S')
            end_a = datetime.strptime(a[1], '%Y-%m-%d %H:%M:%S')
            for ca, aa in enumerate(list_adls):
                if aa == adl:
                    break
            # print '%s_%s: %s - %s' %(ca, adl, start_a, end_a)
            with open(path_sens+'.csv', 'rb') as csv_sens:
                reader_sens = csv.reader(csv_sens, dialect='excel', delimiter='\t')
                for s in reader_sens:
                    sens = '%s %s %s' %(s[2],s[3],s[4])
                    start_s = datetime.strptime(s[0], '%Y-%m-%d %H:%M:%S')
                    end_s = datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S')
                    for cs, ss in enumerate(list_sens):
                        if ss == sens:
                            break
                    if (start_s >= start_a) and (end_s <= end_a):
                        matrix[ca][cs] += 1
                        # print '\t%s_%s: %s - %s' %(cs, sens, start_s, end_s)
    normalize_matrix(matrix)
    # print_matrix(matrix)
    print '%s : O(Sens|ADLs) calculated' %house_name
    csv_matrix(list_adls, list_sens, matrix, house_name+'_O(Sens|ADLs)')
    return matrix

def ghmm_matrix(sigma, A, B, pi, *seqs):
    m = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)
    print '\n', m
    return m

def ghmm_train(m, train_seq):
    m.baumWelch(train_seq)
    print 'trained with baumWelch method\n'

def ghmm_viterbi(sigma, m, test_seq):
    vt = m.viterbi(test_seq)
    print 'analyzed >test_seq< with viterbi algorithm\n', vt

    my_seq = EmissionSequence(sigma, [1] * 20 + [6] * 10 + [1] * 40)
    vm = m.viterbi(my_seq)
    print
    print 'analyzed >my_seq< with viterbi algorithm\n', vm


def project():

    ### dataset is the list of each house analyzed, in each house:
    ###     house[0] = name house
    ###     house[1] = Description
    ###     house[2] = ADLs
    ###     house[3] = Sensors

    # ordonezA = ['Dataset/OrdonezA','Dataset/OrdonezA_Description','Dataset/OrdonezA_ADLs','Dataset/OrdonezA_Sensors']
    # ordonezA = ['Dataset/OrdonezB','Dataset/OrdonezB_Description','Dataset/OrdonezB_ADLs','Dataset/OrdonezB_Sensors']
    # dataset = [ordonezA, ordonezB]

    test1 = ['Deposet/test1','Deposet/test1_Description','Deposet/test1_ADLs','Deposet/test1_Sensors']
    test2 = ['Deposet/test2','Deposet/test2_Description','Deposet/test2_ADLs','Deposet/test2_Sensors']
    dataset = [test1]

    for house in dataset:
        print 
        for path_file in house:
            ### check the correctness of file
            if ('ADLs' in path_file) or ('Sensors' in path_file):
                check_and_generate_csv(path_file)

        house_name = house[0]
        path_adls = house[2]
        path_sens = house[3]

        temp = obtain_p_adls(path_adls, house_name)
        list_adls = temp[0]
        p_adls = temp[1]
        t_adls = obtain_t_adls(path_adls, list_adls, house_name)

        temp = obtain_list_sens(path_sens, house_name)
        list_sens = temp[0]
        sens_seq = temp[1]
        o_sens_adls = obtain_o_sens_adls(path_adls, list_adls, path_sens, list_sens, house_name)

        e = IntegerRange(0, len(list_sens)) ### emission domain
        # print sens_seq
        # real_seq = [1, 2, 3, 4, 5, 6, 7, 8, 6, 7, 9, 10, 3, 11, 3, 4, 12, 12, 6, 11, 4]
        train_sens_seq = EmissionSequence(e, sens_seq)
        # test = [3, 8, 2, 3, 4, 5, 2, 2, 7, 0, 11, 2]
        # test_sens_seq = EmissionSequence(e, test)

        mm = ghmm_matrix(e, t_adls, o_sens_adls, p_adls)
        # ghmm_train(mm, train_sens_seq)
        # ghmm_viterbi(e, mm, test_sens_seq)

    ### //////////////////////////////////////////////
    ### example from ghmm.org
    print '//////////////////////////////////////////////'
    print 'example from ghmm.org'

    sigma = IntegerRange(1, 7)
    A = [[0.9, 0.1], [0.3, 0.7]]
    efair = [1.0 / 6] * 6
    eloaded = [3.0 / 13, 3.0 / 13, 2.0 / 13, 2.0 / 13, 2.0 / 13, 1.0 / 13]
    B = [efair, eloaded]
    pi = [0.5] * 2
    tr = [1, 6, 2, 5, 5, 4, 5, 1, 2, 1, 3, 6, 6, 3, 2, 1, 4, 4, 1, 1, 4, 2, 1, 1, 6, 3, 3, 2, 1, 4, 4, 3, 3, 5, 3, 3, 3, 3, 4, 3, 1, 5, 4, 1, 4, 5, 1, 1, 3, 4, 3, 5, 5, 1, 5, 2, 1, 5, 3, 6, 3, 6, 5, 6, 5, 3, 3, 1, 2, 6, 3, 3, 2, 2, 5, 4, 1, 5, 6, 3, 3, 5, 1, 5, 2, 3, 1, 1, 1, 5, 6, 4, 5, 5, 1, 6, 2, 6, 5, 3, 1, 1, 3, 3, 1, 1, 2, 5, 2, 3, 2, 4, 1, 5, 5, 5, 4, 6, 5, 6, 3, 1, 6, 1, 5, 4, 3, 1, 3, 1, 2, 6, 3, 5, 2, 1, 3, 6, 4, 4, 4, 4, 3, 5, 1, 6, 4, 4, 3, 5, 1, 5, 5, 5, 5, 6, 5, 1, 6, 1, 1, 4, 1, 4, 2, 6, 6, 2, 5, 4, 5, 5, 4, 3, 3, 6, 5, 4, 1, 5, 3, 3, 3, 2, 5, 6, 2, 3, 3, 5, 1, 3, 4, 5, 1, 6, 3, 2, 4, 5, 2, 2, 5, 1, 4, 5, 1, 5, 6, 5, 3, 4, 6, 1, 3, 2, 4, 6, 6, 3, 1, 6, 5, 2, 5, 4, 4, 4, 4, 2, 6, 3, 3, 2, 1, 1, 6, 5, 3, 3, 3, 4, 5, 6, 1, 6, 2, 3, 1, 4, 6, 5, 3, 1, 2, 4, 6, 2, 6, 2, 1, 2, 6, 5, 6, 1, 4, 4, 1, 5, 5, 5, 3, 4, 4, 5, 2, 2, 5, 1, 2, 1, 3, 2, 3, 3, 3, 5, 3, 5, 2, 3, 5, 5, 5, 2, 6, 2, 5, 6, 4, 5, 4, 4, 3, 3, 6, 2, 3, 2, 2, 6, 1, 1, 1, 4, 1, 2, 6, 1, 4, 5, 2, 6, 2, 6, 6, 3, 2, 4, 2, 2, 2, 3, 3, 4, 4, 1, 1, 1, 5, 3, 4, 3, 5, 3, 3, 3, 4, 6, 1, 1, 6, 4, 2, 4, 6, 4, 1, 5, 1, 4, 5, 5, 4, 6, 1, 3, 5, 1, 5, 3, 1, 6, 6, 3, 3, 2, 4, 4, 3, 1, 2, 5, 3, 5, 4, 5, 3, 2, 2, 6, 4, 4, 2, 6, 4, 6, 1, 4, 6, 3, 3, 4, 6, 3, 2, 3, 5, 3, 5, 4, 2, 2, 2, 1, 4, 1, 5, 1, 1, 1, 6, 6, 3, 4, 4, 5, 1, 2, 4, 3, 3, 1, 1, 5, 6, 1, 3, 4, 6, 2, 4, 5, 2, 1, 1, 2, 6, 5, 4, 3, 5, 4, 5, 2, 5, 1, 1, 5, 4, 3, 6, 5, 3, 6, 4, 2, 3, 5, 1, 4, 6, 1, 2, 6, 1, 3, 5, 2, 1, 2, 6, 1, 2, 5, 4, 4, 5, 5, 1, 4, 3, 1, 6, 5, 4, 3, 4, 2, 4, 2, 6, 6, 3, 3, 6, 1, 5, 6, 4, 1, 3, 2, 2, 1, 3, 4, 6, 3, 5, 5, 1, 5, 5, 2, 5, 3, 3, 1, 3, 4, 2, 1, 1, 2, 1, 5, 1, 5, 4, 2, 6, 3, 5, 6, 6, 2, 2, 5, 6, 1, 5, 3, 1, 2, 1, 2, 3, 4, 5, 5, 4, 3, 3, 3, 4, 6, 2, 5, 2, 5, 5, 3, 1, 4, 3, 6, 2, 5, 6, 3, 4, 2, 6, 2, 5, 1, 3, 1, 2, 2, 1, 4, 1, 6, 1, 4, 5, 5, 5, 2, 3, 2, 5, 1, 6, 2, 5, 5, 1, 4, 4, 6, 1, 3, 1, 1, 4, 3, 1, 2, 1, 1, 1, 4, 2, 2, 2, 1, 2, 3, 5, 5, 4, 4, 4, 6, 3, 6, 4, 3, 5, 2, 4, 4, 5, 6, 2, 6, 5, 5, 3, 1, 5, 4, 4, 1, 5, 3, 3, 1, 2, 6, 3, 6, 6, 6, 6, 1, 1, 3, 2, 5, 6, 4, 3, 4, 6, 5, 2, 2, 1, 2, 5, 5, 6, 1, 5, 2, 5, 6, 2, 4, 5, 4, 2, 5, 5, 4, 3, 4, 1, 6, 1, 1, 6, 2, 2, 1, 3, 4, 3, 1, 1, 6, 1, 1, 1, 4, 4, 4, 1, 5, 6, 4, 4, 2, 1, 4, 6, 6, 2, 3, 6, 2, 4, 3, 4, 3, 3, 3, 4, 1, 2, 4, 3, 3, 6, 2, 4, 1, 1, 2, 5, 4, 6, 3, 1, 2, 1, 3, 2, 1, 3, 6, 2, 2, 2, 5, 1, 1, 6, 6, 6, 1, 4, 2, 6, 2, 3, 3, 2, 4, 1, 2, 5, 2, 6, 3, 5, 6, 2, 1, 3, 6, 5, 1, 4, 1, 4, 6, 4, 4, 4, 2, 2, 3, 6, 4, 6, 5, 4, 2, 2, 5, 5, 3, 4, 2, 3, 3, 6, 6, 3, 1, 5, 5, 5, 6, 4, 2, 6, 5, 4, 5, 6, 3, 1, 1, 5, 4, 5, 5, 3, 5, 3, 2, 2, 1, 3, 3, 6, 5, 3, 5, 1, 2, 5, 2, 4, 1, 5, 2, 1, 2, 5, 3, 1, 3, 4, 4, 1, 5, 1, 3, 1, 2, 6, 3, 6, 1, 3, 5, 2, 6, 6, 5, 2, 3, 6, 3, 3, 4, 5, 1, 6, 4, 2, 4, 1, 4, 3, 3, 4, 2, 3, 1, 6, 2, 4, 3, 5, 2, 2, 4, 5, 1, 3, 2, 2, 1, 6, 3, 2, 1, 2, 1, 5, 4, 2, 1, 4, 5, 5, 3, 4, 4, 6, 5, 3, 6, 5, 3, 6, 5, 6, 3, 3, 5, 3, 3, 2, 4, 2, 6, 3, 2, 6, 5, 5, 5, 3, 3, 1, 2, 5, 1, 3, 6, 3, 3, 5, 1, 4, 4, 4, 2, 3, 4, 2, 6, 1, 6, 1, 4, 3, 2, 1, 3, 5, 4, 6, 5, 6, 6, 6, 4, 2, 4, 3, 5, 1, 1, 1, 5, 4, 6, 2, 2, 4, 3, 2, 1, 6, 2, 1, 6, 1, 6, 5, 1, 6, 4, 3, 6, 5, 4, 4, 1, 3, 4, 3, 1, 6, 4, 4, 2, 1, 2, 5, 5, 1, 4, 3, 2, 3, 2, 1, 4, 6, 3, 6, 6, 1, 5, 3, 6, 1, 3, 6, 6, 5, 3, 2, 4, 6, 2, 4, 4, 4, 2, 4, 4, 3, 6, 5, 3, 4, 1, 3, 3, 1, 6, 1, 4, 1, 6, 3, 5, 2, 1, 5, 4, 2, 4, 6, 1, 4, 3, 1, 1, 3, 2, 5, 5, 1, 1, 5, 3, 4, 3, 1, 3, 2, 5, 6, 2, 1, 3, 2, 6, 3, 6, 4, 4, 3, 5, 3, 2, 5, 2, 3, 2, 4, 2, 6, 2, 4, 6, 5, 5, 2, 3, 5, 6, 4, 3, 1, 3, 3, 2, 2, 2, 3, 6, 1, 6, 3, 1, 6, 3, 1, 3, 1, 1, 1, 4, 3, 1, 5, 4, 6, 2, 1, 6, 2, 2, 2, 1, 5, 5, 1, 2, 5, 5, 2, 5, 2, 4, 5, 1, 5, 5, 6, 6, 5, 3, 5, 6, 2, 5, 5, 5, 1, 2, 2, 4, 2, 4, 5, 5, 1, 4, 1, 5, 3, 5, 1, 4, 2, 1, 2, 2, 2, 4, 4, 4, 4, 2, 1, 1, 4, 5, 4, 1, 2, 2, 3, 5, 6, 4, 1, 1, 1, 3, 6, 1, 2, 4, 3, 2, 3, 2, 3, 6, 6, 3, 4, 4, 4, 6, 6, 2, 6, 6, 3, 2, 3, 5, 1, 2, 4, 1, 3, 5, 5, 1, 2, 5, 1, 5, 6, 2, 6, 2, 1, 1, 4, 4, 2, 1, 5, 2, 3, 4, 4, 2, 5, 2, 5, 5, 5, 3, 1, 4, 6, 6, 5, 5, 1, 3, 3, 6, 5, 6, 2, 1, 1, 1, 5, 4, 3, 1, 1, 2, 1, 3, 1, 6, 1, 5, 1, 2, 6, 1, 2, 2, 2, 5, 1, 2, 6, 5, 2, 2, 1, 3, 6, 2, 6, 1, 1, 6, 3, 5, 2, 6, 3, 1, 1, 4, 3, 5, 2, 3, 2, 4, 5, 1, 2, 5, 5, 3, 1, 4, 4, 5, 5, 5, 3, 2, 1, 3, 1, 3, 2, 2, 5, 6, 5, 2, 2, 6, 4, 1, 4, 2, 3, 5, 2, 5, 5, 6, 4, 6, 4, 3, 5, 4, 3, 5, 2, 6, 5, 5, 5, 1, 4, 6, 5, 3, 5, 5, 4, 5, 4, 4, 3, 1, 6, 4, 1, 5, 5, 6, 3, 2, 4, 3, 4, 4, 4, 5, 3, 3, 4, 2, 5, 3, 6, 1, 4, 5, 5, 6, 1, 4, 1, 1, 2, 2, 1, 3, 5, 1, 1, 2, 1, 2, 1, 1, 2, 3, 1, 3, 5, 5, 6, 4, 3, 5, 6, 1, 3, 4, 5, 6, 3, 1, 5, 4, 2, 3, 2, 6, 4, 6, 6, 6, 4, 1, 5, 1, 6, 4, 6, 6, 1, 3, 1, 4, 6, 2, 1, 4, 2, 4, 4, 4, 6, 6, 1, 6, 3, 6, 5, 3, 5, 3, 5, 6, 6, 1, 6, 2, 2, 1, 6, 1, 1, 1, 6, 3, 3, 6, 5, 1, 1, 4, 4, 2, 6, 5, 3, 4, 6, 5, 4, 2, 2, 1, 5, 3, 5, 5, 5, 4, 4, 6, 4, 4, 3, 1, 1, 6, 2, 3, 3, 3, 6, 5, 2, 1, 3, 1, 4, 4, 2, 3, 1, 2, 6, 1, 6, 4, 4, 3, 1, 4, 6, 1, 5, 4, 5, 3, 2, 2, 5, 5, 3, 6, 1, 2, 5, 5, 5, 4, 4, 4, 5, 1, 2, 4, 1, 6, 4, 3, 4, 4, 2, 4, 3, 4, 3, 5, 2, 3, 2, 3, 6, 6, 5, 2, 5, 5, 1, 4, 3, 5, 6, 5, 5, 1, 5, 3, 1, 3, 2, 2, 5, 6, 2, 6, 6, 4, 5, 2, 3, 1, 5, 5, 2, 2, 6, 5, 2, 5, 5, 3, 4, 6, 2, 1, 5, 6, 3, 2, 3, 2, 6, 6, 1, 4, 6, 5, 6, 6, 6, 5, 6, 6, 3, 6, 6, 4, 5, 5, 4, 6, 5, 2, 6, 6, 3, 3, 3, 3, 6, 5, 5, 6, 1, 3, 6, 1, 1, 1, 3, 4, 4, 4, 1, 4, 6, 6, 1, 5, 4, 1, 3, 2, 4, 5, 3, 6, 2, 3, 3, 3, 4, 5, 3, 2, 4, 4, 2, 3, 6, 4, 6, 6, 1, 2, 1, 2, 3, 1, 6, 5, 4, 4, 4, 5, 6, 6, 1, 5, 4, 1, 4, 3, 2, 1, 3, 2, 3, 1, 6, 5, 2, 3, 6, 6, 1, 1, 5, 2, 2, 1, 3, 2, 5, 2, 6, 5, 4, 5, 2, 2, 1, 6, 3, 1, 5, 1, 6, 4, 6, 3, 3, 1, 1, 4, 4, 6, 4, 2, 1, 6, 2, 4, 3, 4, 4, 5, 5, 2, 1, 4, 3, 5, 6, 6, 6, 2, 5, 6, 2, 3, 2, 4, 5, 6, 3, 3, 5, 4, 1, 1, 1, 2, 5, 6, 1, 4, 5, 3, 4, 2, 1, 6, 6, 4, 2, 6, 4, 3, 1, 2, 4, 2, 4, 6, 5, 6, 5, 6, 4, 4, 1, 2, 4, 6, 6, 1, 5, 2, 3, 2, 1, 5, 4, 1, 4, 4, 3, 6, 4, 6, 1, 6, 6, 2, 3, 5, 4, 3, 2, 1, 4, 3, 2, 2, 4, 5, 2, 1, 6, 1, 6, 1, 5, 1, 3, 1, 1, 6, 5, 6, 6, 6, 4, 6, 3, 4, 1, 4, 1, 1, 6, 3, 1, 3, 3, 4, 5, 2, 5, 4, 3, 1, 5, 5, 6, 6, 6, 5, 3, 6, 2, 4, 5, 6, 2, 3, 2, 3, 1, 3, 6, 4, 4, 5, 5, 5, 3, 1, 1, 6, 1, 4, 1, 2, 3, 3, 2, 3, 4, 1]
    train_seq = EmissionSequence(sigma, tr)
    test_seq = EmissionSequence(sigma, [4, 6, 1, 1, 5, 2, 5, 3, 4, 2, 1, 6, 1, 5, 5, 5, 6, 2, 4, 3, 4, 3, 4, 1, 3, 4, 2, 2, 3, 3, 2, 6, 6, 3, 6, 4, 1, 4, 4, 4, 6, 2, 1, 1, 2, 2, 2, 3, 5, 1, 2, 1, 4, 2, 6, 1, 6, 4, 4, 1, 1, 4, 6, 5, 1, 2, 5, 6, 3, 5, 1, 1, 2, 2, 1, 1, 5, 4, 6, 6, 3, 5, 4, 4, 4, 3, 3, 6, 6, 2, 1, 2, 1, 3, 2, 6, 2, 4, 2, 4])
    test_vit = []

    m = ghmm_matrix(sigma, A, B, pi)
    ghmm_train(m, train_seq)
    ghmm_viterbi(sigma, m, test_seq)

    ### //////////////////////////////////////////////

if __name__ == '__main__':
    project()
