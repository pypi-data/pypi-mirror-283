
## Getting started

```
pip install radman
```



## Example

os.makedirs(self.settings.CACHE_PATH,exist_ok=True)

base_url = self.settings.RADMAN_URL
username = self.settings.RADMAN_USER
password = self.settings.RADMAN_PASS

radman = Radman(base_url, username, password)
report_start = self.settings.REPORT_PERIOD['previous']['start']
report_end = self.settings.REPORT_PERIOD['current']['end']
query_params = {
    'filter1': f'study_date,bt,{report_start},{report_end}',
    'join' : 'study,series,instance'
}
print(query_params)
result = radman.run_query("study_ct", query_params)
if result:
    with open(self.data_json_path, 'w') as file:
        json.dump(result, file)
    print("Query result saved")
