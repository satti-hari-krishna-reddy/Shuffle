import requests
import json

from walkoff_app_sdk.app_base import AppBase

class HttpMethod(AppBase):
    __version__ = "1.0.0"
    app_name = "HttpMethod"  

    def __init__(self, redis, logger, console_logger=None):
        print("INIT")
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def fix_url(self, url):
       
        if "hhttp" in url:
            url = url.replace("hhttp", "http")

        if "http:/" in url and not "http://" in url:
            url = url.replace("http:/", "http://", -1)
        if "https:/" in url and not "https://" in url:
            url = url.replace("https:/", "https://", -1)
        if "http:///" in url:
            url = url.replace("http:///", "http://", -1)
        if "https:///" in url:
            url = url.replace("https:///", "https://", -1)
        if not "http://" in url and not "http" in url:
            url = f"http://{url}" 

        return url
    
    def checkverify(self, verify):
        if str(verify).lower().strip() == "false":
            return False
        elif verify == None:
            return False
        elif verify:
            return True
        elif not verify:
            return False
        else:
            return True 

    def is_valid_method(self , method):

           valid_methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]

           method = method.upper()

           if method in valid_methods:
               return method
           else:
             raise ValueError(f"Invalid HTTP method: {method}")

    def parse_content(self, headers):
        parsed_headers = {}
        if headers:
            split_headers = headers.split("\n") 
            self.logger.info(split_headers)
            for header in split_headers:
                if ":" in header:
                    splititem = ":"
                elif "=" in header:
                    splititem = "="
                else:
                    self.logger.info("Skipping header %s as its invalid" % header)
                    continue

                splitheader = header.split(splititem)
                if len(splitheader) >= 2:
                    parsed_headers[splitheader[0].strip()] = splititem.join(splitheader[1:]).strip()
                else:
                    self.logger.info("Skipping header %s with split %s cus only one item" % (header, splititem))
                    continue

        return parsed_headers

    def http_method(self, method = "", headers = "", base_url = "", path = "", username="", password="", verify= True, queries="" , req_body=""):
            
            url = self.fix_url(base_url)

            try : 
                method = self.is_valid_method(method)
            except ValueError as e:
                self.logger.error(e)
                return {"error": str(e)} 

            if path:
               url += '/' + path

            parsed_headers = self.parse_content(headers)
            parsed_queries = self.parse_content(queries)
            
            verify = self.checkverify(verify)

            if isinstance(req_body, dict):
               try:
                  req_body = json.dumps(req_body)

               except json.JSONDecodeError as e:
                  self.logger.error(f"error : {e}")
                  return {"error: Invalid JSON format for request body"}
            
            auth=None
            if username or password:      
                if "Authorization" in headers:
                     pass
                else: 
                    auth = requests.auth.HTTPBasicAuth(username, password)

            try:
                  response = requests.request(method, url, headers = parsed_headers, params=parsed_queries, data = req_body, auth = auth , verify = verify)
                  response.raise_for_status()
                  return response.json()

            except requests.RequestException as e:
                    self.logger.error(f"Request failed: {e}")
                    return {"error": f"Request failed: {e}"}


if __name__ == "__main__":
    HttpMethod.run()