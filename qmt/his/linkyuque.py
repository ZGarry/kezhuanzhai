import requests
headers = {
	"Content-Type": "application/json",
	"User-Agent": "YQExportMD",
	"X-Auth-Token": 'pOjxLEomTonND2KSTHDMbAqPyn2oxmak5UhjWTID'
}	
response = requests.request(method='GET', url='https://www.yuque.com/api/v2/users/zfjz/repos', headers=headers)
response.json()