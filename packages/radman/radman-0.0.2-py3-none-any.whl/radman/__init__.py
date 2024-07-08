import requests

class Radman:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.logged_in = False

    def login(self):
        login_url = f'{self.base_url}/login.php'
        login_data = {
            'username': self.username,
            'password': self.password
        }

        try:
            response = self.session.post(login_url, data=login_data)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            self.logged_in = True
            print("Logged in successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Login failed. An error occurred: {e}")


    def run_query(self, table, query_params=None):
        if not self.logged_in:
            self.login()

        headers = {
            'Content-Type': 'application/json'
        }
        
        if query_params is None:
            query_params = {
                'page': '1,100'  # Default page is 1,100
            }
        elif 'page' not in query_params:
            query_params['page'] = '1,500'  # Default page is 1,100

        all_results = []
        page_range = query_params['page'].split(',')
        page_number = int(page_range[0])
        page_size = int(page_range[1])
        
        while True:
            try:
                response = self.session.get(f'{self.base_url}/api/rest.php/records/{table}', params=query_params, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
                
                result = response.json()
                if not result["records"]:
                    break  # No more records, stop fetching
                
                print(f"Page {page_number},{page_size} - Query result fetched")
                all_results.extend(result["records"])
                page_number += 1
                query_params['page'] = f"{page_number},{page_size}"
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while running the query: {e}")
                break
        
        return all_results
    
    def fetch_dicom_file(self, instance_id):
        if not self.logged_in:
            self.login()

        try:
            response = self.session.get(f'{self.base_url}/api/instance-file.php', params={'id': instance_id})
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            return response.content  # Return the raw DICOM file content
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the DICOM file: {e}")
            return None

    def logout(self):
        if self.logged_in:
            logout_url = f'{self.base_url}/logout.php'
            try:
                response = self.session.post(logout_url)
                response.raise_for_status()
                self.logged_in = False
                print("Logged out successfully.")
            except requests.exceptions.RequestException as e:
                print(f"Logout failed. An error occurred: {e}")