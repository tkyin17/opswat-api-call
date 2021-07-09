# opswat_api_call
OPSWAT api calls to metadefender api to obtain scan reports using hash values or dataid of a given file, and also upload the file if it does not already exist on the server

# Setup

- Before running the program, replace 'KEY' in the api_headers and upload_headers dict with a valid api key.

- Requires the 'requests' and 'hashlib' python modules to be installed

![image](https://user-images.githubusercontent.com/59483688/125090423-50803980-e09d-11eb-869c-b9b93a2b221e.png)


# To run:

* The program uses md5 hashing method by default. To change to one of the other methods, at the bottom of the .py file, uncomment and comment the respective lines required before running the program.

![image](https://user-images.githubusercontent.com/59483688/125092380-4eb77580-e09f-11eb-81dc-64cbdd3cdbd7.png)

* execute the following terminal command: python3 api_call.py file-path


Examples:

* python3 api_call.py sample.txt

* python3 api_call.py C:\Users\name\Desktop\sample.txt


# Details

The program will read in the target file as bytes, compute the hash value of the specified hash methods (md5, sha1, or sha256), send a request to the metadefender api to retrieve the scan results, and if found, will print some information from the scan report including the status of the file, engines used to scan, number of threats found.

If the hash is not found in the metadefender server, then the file must be uploaded to the server to be scanned. The program will automatically attempt to upload the file if no matching hash value was found. Then the program will continuously poll the server by sending a scan report retrieval request using dataid. If the scan is still inqueued, then the program will continue polling until the file scan is completed and the scan report is successfully retrieved.

The scan reports appears to have different json formatting depending on the scan result code. From the example documentations, I concluded that the scan reports in which the file is safe, contains a threat, or is suspicious will likely have the same formatting therefore I am able to print the corresponding key:value info from the json dict. However, for other scan result code, I was unable to find out what the json formatting looks like due to the daily 5 upload file for trial OPSWAT accounts preventing me from performing additional tests.

From available testing, one scan report contained scan result code 10 which contained less info than the normal scan report. Code 10 in particular means that the scan was not executed which resulted in the scan report being incomplete. No details on why the scan was skipped were mentioned in the scan report.

Based on this scenario, I had all scan result code that I was unable to view the json format of simply print the scan result code along with the associated message instead of attempting to print the json information. Otherwise, the program will halt when it attempts to print a key:value that is not available in a specific scan report associated with the scan result codes that I do not know the json formatting of.


Example output:


![image](https://user-images.githubusercontent.com/59483688/125090000-df408680-e09c-11eb-9469-b8ae88ab41af.png)
