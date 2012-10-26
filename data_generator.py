import urllib2
import json
from BeautifulSoup import BeautifulSoup,Tag

def calculateKHL(team):
    league = 'Russia'
    if(team == 'HC Lev Praha'):
        league = 'Czech Republic'
    if(team == 'Atlant Mytishchi'):
        league = 'Russia'
    if(team == 'HC Slovan Bratislava'):
        league = 'Slovakia'
    if(team == 'HC Donbass'):
        league = 'Ukraine'
    if(team == 'Lev Praha'):
        league = 'Czech Republic'
    if(team == 'Lokomotiv Yaroslavl'):
        league = 'Russia'
    if(team == 'St. Petersburg'):
        league = 'Russia'
    if(team == 'Avangard Omsk'):
        league = 'Russia'
    if(team == 'Severstal Cherepovets'):
        league = 'Russia'
    if(team == 'CSKA Moscow'):
        league = 'Russia'
    if(team == 'Neftekhimik'):
        league = 'Russia'
    if(team == 'Dinamo Minsk'):
        league = 'Belarus'
    if(team == 'Ak Bars Kazan'):
        league = 'Tatarstan'
    if(team == 'Vityaz Chekhov'):
        league = 'Russia'
    if(team == 'Chelyabinsk'):
        league = 'Russia'
    if(team == 'Torpedo Nizhny Novgorod'):
        league = 'Russia'
    if(team == 'Bratislava'):
        league = 'Slovakia'
    if(team == 'Barys Astana'):
        league = 'Kazakhstan'
    if(team == 'Dinamo Riga'):
        league = 'Latvia'
    if(team == 'Metallurg'):
        league = 'Russia'
    if(team == 'Barys Astana'):
        league = 'Kazakhstan'
    if(team == 'Dynamo Moscow'):
        league = 'Russia'
    return league


page = urllib2.urlopen("http://www.sportsnet.ca/hockey/nhl-lockout/nhl_players_in_europe/")
soup = BeautifulSoup(page)

tables = soup.findAll("table", { "class" : "stats" })
data = {}
for table in tables:
	for row in table.findAll('tr'):
		#the first row has a 'first-row' class that we can ignore
		if not row.has_key('class'):
		    columns = row.findAll('td')
		    #the rows with 4 columns contain the good stuff
		    if(len(columns) == 4):
			    player = columns[0].contents[0]
			    position = columns[1].contents[0]
			    team = columns[2].contents[0]
			    league = columns[3].contents[0]
			    #filter out (Division 1|2)
			    if(league.find("(Division") > 0):
				    league = league[0:league.find("(Division")]
			    if(league.find("(I") > 0):
                                    league = league[0:league.find("(I")]
			    #make the league line up better with what is in the europe.json
			    if(league == 'Czech'):
                                league = 'Czech Republic'
			    if(league == 'England'):
                                league = 'United Kingdom'
			    if(league == 'Swiss'):
                                league = 'Switzerland'
			    if(league == 'Austrian Hockey League'):
                                league = 'Austria'
                            if(league == 'UK Elite Ice Hockey League'):
                                league = 'United Kingdom'
                            if(league == 'KHL'):
                                league = calculateKHL(team)
                            #build the return object
                            if league in data:
                                countryMap = data[league]
                                playerList = countryMap['players']
                                playerList.append({'name':player,'team':team})
                                countryMap['players'] = playerList
                                countryMap['count'] = countryMap['count'] + 1
                                data[league] = countryMap
                            else:
                                countryMap = {'players':[{'name':player,'team':team}],'count':1}
                                data[league] = countryMap
                            
data = {'countries':data}
f = open('data.json','w')
f.write(json.dumps(data))
f.close()





