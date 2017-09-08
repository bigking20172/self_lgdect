import os

if __name__ == '__main__':
    files = os.listdir('/Volumes/self_hd/medicial_sp')
    f_save = open('/Volumes/self_hd/deal_samples/pro_txt.txt','w') 
    
    for line in files:
	if line.find('txt') != -1:
		f_save.writelines(line+'\n')	
    f_save.close()
