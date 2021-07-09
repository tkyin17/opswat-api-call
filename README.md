# opswat_api_call
OPSWAT api calls to metadefender api to obtain scan reports using hash values or dataid, and also upload files if they do not already exist on the server

To run:
python3 api_call.py file

Example:
python3 api_call.py sample.txt

python3 api_call.py C:\Users\name\Desktop\sample.txt


The program will read in the target file as bytes, compute the hash value of the specified hash methods (md5, sha1, or sha256), send a request to the metadefender api to retrieve the scan results, and if found, will print some information from the scan report include the status of the file, engines used to scan, number of threats found.

If the hash is not found in the metadefender server, then the file must be uploaded to the server to be scanned. The program will automatically attempt to upload the file if no matching hash value was found. Then the program will continuously poll the server by sending a scan report retrieval request using dataid. If the scan is still inqueued, then the program continue polling until the file scan is completed and the scan report is successfully retrieved.

The scan reports appears to have different json formatting depending on the scan result code. From the example documentations I concluded that scan reports where the file is safe, contains a threat, or is suspicious will likely have the same formatting therefore I am able to print the corresponding key:value info from the json dict. However, for other scan result code, I was not able to find out what the json formatting looks like due to the daily 5 upload file for trial OPSWAT accounts.

From testing, one scan report contained scan result code 10 which contained less info than the normal scan report. Code 10 in particular means that the scan was not executed which resulted in the scan report being incomplete. No details on why the scan was skipped.

Based on this scenario, I had all scan result code that I was not able to view the json format of simply print the scan result code along with the associated message instead of attempting to print the json information.

Example output:
![image](https://user-images.githubusercontent.com/59483688/125090000-df408680-e09c-11eb-9469-b8ae88ab41af.png)
