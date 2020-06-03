teams = [{
'team_name':'sandi',
'team_data':{'host':'test.com','port':'1337'}			
}]
for team in teams:
	print(team['team_name'],team['team_data']['host'])