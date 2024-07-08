import requests
import pkg_resources
from openredirect.includes import keys
from openredirect.includes import sms
from openredirect.includes import writing
from urllib.parse import quote, urlparse
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#arr_redirection_header=["red","location=","returnUrl=","link=","Next=","image_path=","ret=","toredirect=","redirect_url=","page=","ReturnUrl=","ActionCodeURL=","r2=","redirectBack=","forward=","q=","return_url=","img=","AuthState=","open=","url=","uri=","newurl=","u=","Referer=","file=","redirect=","path=","From=","return=","redir=","langTo=","end_display=","referrer=","rb=","r=","|=","Goto=","url=","file=","old=","URL=","aspxerrorpath=","back="]

def openrescan(url,output=None):
    try:
        with requests.Session() as session:
            # payload_path = pkg_resources.resource_filename('includes', 'payload.txt')
            # with open(payload_path, 'r', encoding='utf-8') as f:
            #     payloads = f.read().splitlines()

            for i in keys.payload:
                payl = quote(i)
                if url.endswith('/'):
                    url = url[:-1]
                full_url = f"{url}/{payl}"
                response = session.get(full_url, verify=False, allow_redirects=False, timeout=5)
                print("Checking ===>",full_url) 
                if response and 'location' in response.headers:                
                    location = response.headers['location']
                    parsed_url = urlparse(location)
                    domain = parsed_url.netloc
                    if response.status_code >= 300 and 'location' in response.headers:
                                output_msg = f"Vulnerable URL: {full_url}"
                                print(output_msg)
                                sms.send_msg(output_msg)
                                if output:
                                    writing.writedata(output,full_url)    
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        # Optionally perform cleanup here
        exit(0)                                     
    except requests.exceptions.RequestException as e:
        print(f"Check Network Connection: {e}")

