import requests
from urllib.parse import urlencode, urlunparse, parse_qs, urlparse

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
            query_params['page'] = '1,500'  # Default page is 1,500

        # Prepare the URL with query parameters
        url_parts = list(urlparse(f'{self.base_url}/api/rest.php/records/{table}'))
        query = parse_qs(url_parts[4])
        
        for key, value in query_params.items():
            if isinstance(value, list):
                query[key] = value
            else:
                query[key] = [value]

        url_parts[4] = urlencode(query, doseq=True)
        url = urlunparse(url_parts)

        all_results = []
        page_range = query_params['page'][0].split(',')
        page_number = int(page_range[0])
        page_size = int(page_range[1])

        while True:
            try:
                response = self.session.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

                result = response.json()
                if not result["records"]:
                    break  # No more records, stop fetching

                print(f"Page {page_number},{page_size} - Query result fetched")
                all_results.extend(result["records"])
                page_number += 1
                query_params['page'] = f"{page_number},{page_size}"
                query['page'] = [query_params['page']]
                url_parts[4] = urlencode(query, doseq=True)
                url = urlunparse(url_parts)
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