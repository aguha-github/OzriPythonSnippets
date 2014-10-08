import httplib, urllib, json

# a class for representing access to the ArcGIS Server Admin rest endpoints
class AgsAdmin:

    def __init__(self, server_name, server_port, user_name, password):
        self.server_name = server_name
        self.server_port = server_port
        self.token = self.get_token(user_name, password)

        if self.token == "":
            print "Could not generate a token with the username and password provided."
            return


    # generate a token given username, password and the adminURL.
    def get_token(self, user_name, password):

        token_url = "/arcgis/admin/generateToken"
        params = urllib.urlencode({'username': user_name, 'password': password, 'client': 'requestip', 'f': 'json'})
        
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        
        http_conn = httplib.HTTPConnection(self.server_name, self.server_port)
        http_conn.request("POST", token_url, params, headers)
        
        response = http_conn.getresponse()
        if (response.status != 200):
            http_conn.close()
            print "Error while fetching tokens from admin URL. Please check the URL and try again."
            return
        else:
            data = response.read()
            http_conn.close()
            
            # Check that data returned is not an error object
            if not self.assert_json_success(data):            
                return
            
            # Extract the token from it
            token = json.loads(data)       
            return token['token']


    def query_logs(self, start_time, end_time, log_filter):

        log_query_url = "/arcgis/admin/logs/query"
        
        params = urllib.urlencode({'level': 'FINE', 'startTime': start_time, 'endTime': end_time, 'filter': log_filter, 'token': self.token, 'f': 'json'})
        
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
           
        http_conn = httplib.HTTPConnection(self.server_name, self.server_port)
        http_conn.request("POST", log_query_url, params, headers)
        
        response = http_conn.getresponse()

        if (response.status != 200):
            http_conn.close()
            print "Error while querying logs."
            return
        else:
            data = response.read()

            # Check that data returned is not an error object
            if not self.assert_json_success(data):          
                print "Error returned by operation. " + data
            else:
                print "Operation completed successfully!"

            # Deserialize response into Python object
            log_data = json.loads(data)
            http_conn.close()

            return log_data            
        

    # checks that the JSON object is not an error object   
    def assert_json_success(self, data):
        obj = json.loads(data)
        if 'status' in obj and obj['status'] == "error":
            print "Error: JSON object returns an error. " + str(obj)
            return False
        else:
            return True