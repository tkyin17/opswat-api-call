from __future__ import print_function
import sys
import hashlib
import requests


# 140mb file size max, no need to use a buffer
# hexadecimal hash values

# code 200 == found
# code 404 == not found

hash_url = 'https://api.metadefender.com/v4/hash/'
upload_url = 'https://api.metadefender.com/v4/file/'

# for retrieving scan reports using hash value and polling
api_headers = {'apikey': '2a798b4d15c55113ad405114994ee716'}

# for upload request
upload_headers = {'apikey': '2a798b4d15c55113ad405114994ee716', 'content-type': 'application/octet-stream', 'sandbox': 'windows10'}

filename = sys.argv[1]

# if the scan is completed, then the details from the scan report will be printed with information
# regarding the engine, threat_found, etc
# other scan report codes might have different format since code 10 has a slightly different json format than
# code 0-2
def print_info(res_dict):
    result_code = res_dict['scan_results']['scan_all_result_i']    
    
    if int(result_code) >= 0 and int(result_code) <= 2:
        print('filename:', res_dict['file_info']['display_name'])
        print('overall_status:', res_dict['scan_results']['scan_all_result_a'], '\n')
        
        engine_list= res_dict['scan_results']['scan_details']
        
        for e in engine_list:
            print('engine:', e)
            print('threat_found:', engine_list[e]['threat_found'] if engine_list[e]['threat_found'] != '' else 'None' )
            print('scan_result:', engine_list[e]['scan_result_i'])
            print('def_time:', engine_list[e]['def_time'], '\n')
            
    else:
        print('Unable to retrieve scan report')
        print('Scan result code:', result_code)
        print('Status:', res_dict['scan_results']['scan_all_result_a'])
        
# binary upload of file, read in file as bytes
def upload_file():
    infile = open(filename, 'rb')
    file = infile.read()
    infile.close()
    
    res = requests.post(upload_url, headers=upload_headers, data=file)
    res_dict = res.json()
    
    if res.status_code == 200:
        # poll until upload is completed
        print('File upload completed. Scanning is in progress.\n')
        return res_dict['data_id']
    else:
        handle_error(res_dict)
              
# searches for scan report by dataid
def poll(dataid):
    print('Retrieving scan reports')
    
    res = requests.get(upload_url+dataid, headers=api_headers)
    res_dict = res.json()
    
    if res.status_code == 200:
        # in_queue response has 'in_queue' key in the json while a completed scan report does not
        # check if 'in_queue' key exists in the json, if it does then scan is in in progress,
        # poll again
        if 'in_queue' in res:
            print('File is inqueue to be scanned, polling again\n')
            return False
        else:
            print_info(res_dict) 
            return True
    else:
        handle_error(res_dict)
        

# print error code and description and exit the program
def handle_error(res_dict):
    print('Error code:', res_dict['error']['code'])
    for i in res_dict['error']['messages']: print('--',i)
    
    print('\nExiting program')
    sys.exit()

# run the hash method based on the string value of 'name'
# if the hash is not found, then upload the file and poll until scan report is recieved 
# if scanning is in inqueue
def run(name):
    hasher = None
    
    if name.lower() == 'md5':
        hasher = hashlib.md5()
    elif name.lower() == 'sha1':
        hasher = hashlib.sha1()
    elif name.lower() == 'sha256':
        hasher = hashlib.sha256()
    
    with open(filename, 'rb') as infile:
        file = infile.read()
        hasher.update(file)
        
    # returns the hexadecimal value of the hash result
    result = hasher.hexdigest()
    res = requests.get(hash_url+result, headers=api_headers)
    res_dict = res.json()
    
    if res.status_code == 200:
        print_info(res_dict)
    elif res.status_code == 404:
        print('Error code 404: The hash was not found')
        print('Proceeding to upload the file\n')
        dataid = upload_file()
        
        while True:
            b = poll(dataid)
            if b:
                break
    else:
        handle_error(res_dict)

run('md5')
#run('sha1')
#run('sha256')