#!/usr/bin/env python

import os
import subprocess
import copy
import sys

def mergeTwoFiles(file1, file2, header1, header2, key1, key2, output1, output2, output3):
    # merge two files by the key
    # output1 has the matching info
    # output2 has the info in file1 but not in file2
    # output3 has the info in file2 but not in file1

    # check if output files are existing. If they are, remove them
    for outputfile in [output1, output2, output3]:
        if os.path.isfile(outputfile):
    	    subprocess.Popen('rm '+outputfile, shell=True).wait()

    #print "Please make sure that the two files are sorted by the key given."
    with open(file1, 'r') as f, open(file2, 'r') as g, open(output1, 'wb') as o1, \
         open(output2, 'wb') as o2, open(output3, 'wb') as o3:
        # compute the length of the two files
        L1 = int(subprocess.check_output(['wc', '-l', file1]).strip().split()[0])
	L2 = int(subprocess.check_output(['wc', '-l', file2]).strip().split()[0])

        # init
	cursor1 = 0
	cursor2 = 0
        data1 = {header1[i]:[] for i in range(len(header1))}
	data2 = {header2[i]:[] for i in range(len(header2))}

        count = 0
        while True:
            # process until both of the files have been processed

	    # init for the first line of both files
	    if cursor1 == 0 and cursor2 == 0:
	        # file1
	        line1 = f.readline()
		elements1 = line1.strip().split('\t')
		row1 = {header1[i]:elements1[i] for i in range(len(header1))}
		for h in header1:
		    data1[h].append(row1[h])

		last_key1 = []
		for key in key1:
		    last_key1.append(row1[key])
                cursor1 += 1
		this_key1 = copy.copy(last_key1)

		read_flag1 = True
		end_flag1 = False
		

                # file2
	        line2 = g.readline()
		elements2 = line2.strip().split('\t')
		row2 = {header2[i]:elements2[i] for i in range(len(header2))}

		for h in header2:
		    data2[h].append(row2[h])

		last_key2 = []
		for key in key2:
		    last_key2.append(row2[key])
		cursor2 += 1

		this_key2 = copy.copy(last_key2)

		read_flag2 = True
		end_flag2 = False
		

            else: # for the rest of the two files 
		while read_flag1 == True:
	            last_key1 = copy.copy(this_key1)
		    # if the keys remain the same in file1, proceed to read the next line
		    line1 = f.readline()
		    if line1 == "":
		        end_flag1 = True
			break
		    elements1 = line1.strip().split('\t')
		    row1 = {header1[i]:elements1[i] for i in range(len(header1))}
		    #print "c1: "+line1
		    cursor1 += 1
		   
		    this_key1 = []
		    for key in key1:
		        this_key1.append(row1[key])
                    if cmp(this_key1, last_key1) ==0:
		        for h in header1:
		            data1[h].append(row1[h])

		    else:		       # new key appears. 
		        read_flag1 = False
		    

	        while read_flag2 == True:
		    # if the keys remian the same in file2, proceed to read the next line
		    last_key2 = copy.copy(this_key2)
		    line2 = g.readline()
		    if line2 == "":
		        end_flag2 = True
		        break
		    elements2 = line2.strip().split('\t')
		    row2 = {header2[i]:elements2[i] for i in range(len(header2))}
		    #print "        c2: "+line2
		    cursor2 += 1

		    this_key2 = []
		    for key in key2:
		        this_key2.append(row2[key])

                    if cmp(this_key2, last_key2) == 0:
		        for h in header2:
		            data2[h].append(row2[h])


		    else:
		        # new key appears
			read_flag2 = False

	        # by this point, the chunks with the same keys in file1 and file2 have been read
		# we need to process the data
		header2but1 = copy.copy(header2)

		for key in key2:
		    header2but1.remove(key)
		
		
                #print data1, data2, cursor1, L1, cursor2, L2 

		if (cmp(last_key1, last_key2) < 0 or data2=={}) and (data1 != {}):
	            #print 'case1'
		    # last_key1 < last_key2 indicates that, there is not information in file2 that corresponds to key1
		    # then put info in data1 in, and leave NA for columns in data2
                    # the outputfile is output2

		    n1 = len(data1[header1[0]]) # num of rows in data1


		    for i in range(n1):
		        str1 = ""
		        for h in header1:
		            str1 += data1[h][i] + '\t'

		        for h in header2but1[:-1]:
		            str1 += 'NA' + '\t'
		       
		        str1 += 'NA' + '\n'
		        o2.write(str1)

		    read_flag1 = True # proceed to read more in the file1
		    if not end_flag1: 
		        data1 = {header1[i]:[] for i in range(len(header1))}
		        last_key1 = copy.copy(this_key1)
		        for h in header1:
		            data1[h].append(row1[h])
	            else:
		        data1 = {}


                 
	        elif (cmp(last_key1, last_key2) > 0 or data1=={}) and (data2 !={}):
		    #print 'case2'
		    # last key 2 > last key1, indicates that, there is no information in file1 that corresponds to key2
                    # the outputfile is output3

		    n2 = len(data2[header2[0]])
		    for i in range(n2):
		        str1 = ""
			for h in header1:
			    if h in key1:
			        ind = key1.index(h) # find the position
				str1 += data2[key2[ind]][i] + '\t' # fill in the info of B into the key columns
			    else:
			        str1 += 'NA' + '\t'
		        for h in header2but1[:-1]:
			    str1 += data2[h][i] + '\t'

			str1 += data2[header2but1[-1]][i] + '\n'
		   	o3.write(str1)

		    read_flag2 = True # proceed to read more in the file2
		    if not end_flag2:
	                data2 = {header2[i]:[] for i in range(len(header2))}
		        last_key2 = copy.copy(this_key2)
		        for h in header2:
		            data2[h].append(row2[h])
	            else:
		        data2 = {}

                else:
		# last_key1 == this_key1
		# the keys of the data match, so it's good to proceed the matching

		    #print 'case3'

		    n1 = len(data1[header1[0]])
		    n2 = len(data2[header2[0]])

		    if n1 > 1 and n2 > 1:
		        print "[Fatal Error] Unique Key Error!"

		    if n1 < n2:
		        #data1 has fewer lines
			record1 = [data1[h][0] for h in header1]

			for ind in range(n2):
			    str1 = ""

			    for r in record1:
			        str1 += r + '\t' 
			    for h in header2:
			        if h not in key2:
			            str1 += data2[h][ind] + '\t'
		            str1 += str1[:-1] + '\n'
			    o1.write(str1)


	            if n2 <= n1:
		        # data2 has fewer lines
			record2 = []
		        for h in header2:
                            if h not in key2:
			        record2.append(data2[h][0])
			for ind in range(n1):
			    str1 = ""
			    for h in header1:
			        str1 += data1[h][ind] + '\t'
			    for ele in record2:
			        str1 += ele + '\t'
			    str1 = str1[:-1] + '\n'
			    o1.write(str1)

		    read_flag1 = True
		    read_flag2 = True
		    if not end_flag1: 
		        data1 = {header1[i]:[] for i in range(len(header1))}
		        last_key1 = copy.copy(this_key1)
		        for h in header1:
		            data1[h].append(row1[h])
	            else:
		        data1 = {}

		    if not end_flag2:
	                data2 = {header2[i]:[] for i in range(len(header2))}
		        last_key2 = copy.copy(this_key2)
		        for h in header2:
		            data2[h].append(row2[h])
	            else:
		        data2 = {}

 
			    

			    

                # break criteria
		if data1 == {} and data2 == {}:
		   break





def parseRange(str1):

    # given a str1 in the format of 1,2,3-5,6
    # return a list of cols

    tmp = str1.split(',')
    ret = []
    for e in tmp:
        if '-' in e:
	    ends = e.split('-')
	    ret += range(int(ends[0]), int(ends[1])+1)
	
	else:
	    ret.append(int(e))

    return ret

def main(sorted_status=False):
    file1 = sys.argv[1]
    key1 = sys.argv[2]
    show1 = sys.argv[3]
    num_column1 = int(subprocess.check_output("awk '{print NF; exit}' " + file1, shell=True))
    cols1 = range(1, num_column1+1)
    key1 = parseRange(key1)
    show1 = parseRange(show1)


    file2 = sys.argv[4]
    key2 = sys.argv[5]
    show2 = sys.argv[6]
    num_column2 = int(subprocess.check_output("awk '{print NF; exit}' " + file2, shell=True))
    cols2 = range(1, num_column2 + 1)

    output1 = sys.argv[7]

    if len(sys.argv) == 8:
       output2 = 'out2.tsv'
       output3 = 'out3.tsv'
    else:
       output2 = sys.argv[8]
       output3 = sys.argv[8]

    key2 = parseRange(key2)
    show2 = parseRange(show2)
    if not sorted_status: 
        sort_cmd1 = 'gsort -i '
        for k in key1:
            sort_cmd1 +='-k '+str(k)+','+str(k)
        sort_cmd1 += ' '+file1
        sort_cmd2 = 'gsort -i '
        for k in key2:
            sort_cmd2 +='-k' +str(k)+','+str(k)
        sort_cmd2 += ' '+file2

    #print [file1, file2, output1, output2, output3]
    mergeTwoFiles(file1, file2, cols1, cols2, key1, key2, output1, output2, output3)

    output_col = copy.copy(show1)

    for ele in show2:
        if ele not in key2:
	    output_col.append(len(cols1)-len(key2)+int(ele))
    #print output_col
    cut_cmd = 'cut -f '
    for ele in output_col[:-1]:
        cut_cmd += str(ele) + ','

    cut_cmd += str(output_col[-1]) + ' '+ output1
    subprocess.Popen(cut_cmd, shell=True).wait()
    #subprocess.Popen('rm '+output1, shell=True).wait()
    #subprocess.Popen('mv '+output1+'.tmp '+ output1, shell=True).wait() 


    
if __name__ == '__main__':
    main()

		



	



	
	

           

