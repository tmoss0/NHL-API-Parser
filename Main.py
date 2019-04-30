# Import libraries
import urllib.parse
import requests
import json
from datetime import date

# Variable declarations
main_api = "https://statsapi.web.nhl.com/api/v1"
short_api = "https://statsapi.web.nhl.com"
schedule = "/schedule"
roster = "/roster"
stats = "/stats"
teams = "/teams"
nextGame = "?expand=team.schedule.next"
previousGame = "?expand=team.schedule.previous"
regularSeason = "/standings/regularSeason?date=" + str(date.today())

team_api_id = ""
team = ""
link = ""
teamsList = []

####################### USER INPUT #######################
# Print team list to user
def printTeams():
	for num, name in enumerate(teamsList, start = 1):
		print("{} - {}".format(num, name))

# Get user input and show user team selection
def userTeamInput(json_data):
	try:
		selection = int(input("\nEnter number for team: "))
		teamNumber = selection - 1
		print("You've selected", teamsList[teamNumber])
		team = teamsList[teamNumber]
		getTeamAPIID(team)

		for item in json_data["teams"]:
			if item["name"] == teamsList[teamNumber]:
				link = item["link"]
				break

	except ValueError:
		print("\nYou must enter a number")
		userTeamInput(json_data)

	except:
		print("\nNot listed, please try again")
		userTeamInput(json_data)
	
	return link


# Select option to view more information 
def viewMoreInformation(link):
	divider()
	print("\nPlease type the number associated with a category to view more information")
	print("\n1 - Team Stats")
	print("2 - Roster")
	print("3 - Draft History")
	print("4 - Next Game Info")
	print("5 - Previous Game Info")
	print("6 - Regular Season Standings")
	try:
		selection = int(input("\nEnter a number to view more information about a category: "))

		if selection == 1:
			getStatistics(link)
		elif selection == 2:
			getRoster(link)
		elif selection == 3:
			getDraft(link)
		elif selection == 4:
			getNextGame(link)
		elif selection == 5:
			getPreviousGame(link)
		elif selection == 6:
			getRegularSeasonStandings(link)
		else:
			raise Exception

	except ValueError:
		print("\nYou must enter a number")
		viewMoreInformation(link)

	except:
		print("\nError, please try again")
		viewMoreInformation(link)

# Get team statistics
def getStatistics(link):
	parsedData = urlParser(link, stats)
	singleSeasonData = parsedData["stats"][0]["splits"][0]["stat"]
	regularSeasonData = parsedData["stats"][1]["splits"][0]["stat"]

	gamesPlayed = singleSeasonData["gamesPlayed"]
	wins = singleSeasonData["wins"]
	loss = singleSeasonData["losses"]
	ot = singleSeasonData["ot"]
	points = singleSeasonData["pts"]
	savePct = singleSeasonData["savePctg"]
	ppPct = singleSeasonData["powerPlayPercentage"]
	pkPct = singleSeasonData["penaltyKillPercentage"]
	foPct = singleSeasonData["faceOffWinPercentage"]
	goalsAverage = singleSeasonData["goalsPerGame"]
	goalsAgainstAverage = singleSeasonData["goalsAgainstPerGame"]

	savePctRank = regularSeasonData["savePctRank"]
	ppPctRank = regularSeasonData["powerPlayPercentage"]
	pkPctRank = regularSeasonData["penaltyKillPercentage"]
	foPctRank = regularSeasonData["faceOffWinPercentage"]
	goalsPerGameRank = regularSeasonData["goalsPerGame"]
	goalsAgainstPerGameRank = regularSeasonData["goalsAgainstPerGame"]

	# Print team stats
	print("\nRecord: %s-%s-%s" % (str(wins), str(loss), str(ot)))
	print("\nGames played: " + str(gamesPlayed))
	print("Points: " + str(points))
	print()
	print("Goalie save: {} ({})".format(str(savePct), str(savePctRank)))
	print("Power play: {}% ({})".format(str(ppPct), str(ppPctRank)))
	print("Penalty kill: {}% ({})".format(str(pkPct), str(pkPctRank)))
	print("Face off win: {}% ({})".format(str(foPct), str(foPctRank)))
	print()
	print("Goals per game: " + str(goalsAverage) + " (" + str(goalsPerGameRank) + ")")
	print("Goals against per game: " + str(goalsAgainstAverage) + " (" + str(goalsAgainstPerGameRank) + ")")
	print()

# Print the full current team roster for selected team
def getRoster(link): 
	parsedData = urlParser(link, roster)
	rosterData = parsedData["roster"]

	goalie = []
	center = []
	leftWing = []
	rightWing = []
	defenseMan = []
	
	for index, person in enumerate(rosterData):
		# Goalie
		if rosterData[index]["position"]["name"] == "Goalie":
			appendNamesAndNumber(goalie, rosterData, index)
		# Center
		elif rosterData[index]["position"]["name"] == "Center":
			appendNamesAndNumber(center, rosterData, index)
		# Left Wing
		elif rosterData[index]["position"]["name"] == "Left Wing":
			appendNamesAndNumber(leftWing, rosterData, index)
		# Right Wing
		elif rosterData[index]["position"]["name"] == "Right Wing":
			appendNamesAndNumber(rightWing, rosterData, index)
		# Defenseman
		elif rosterData[index]["position"]["name"] == "Defenseman":
			appendNamesAndNumber(defenseMan, rosterData, index)

	# Use printPosition to list players at each position
	printPosition(goalie, "Goalie")
	printPosition(center, "Center")
	printPosition(leftWing, "Left Wing")
	printPosition(rightWing, "Right Wing")
	printPosition(defenseMan, "Defenseman")

# Get draft year of team then return players, draft position, position (if applicable),
# draft round and overall selection 
# def getDraft(link):
	year = input("Please enter a draft year: ")
	draft = "/draft/" + year
	parseUrl = main_api + draft
	json_data = requests.get(parseUrl).json()
	shortenedSearch = json_data["drafts"]

	# Adjust number of teams depending on what year is queried
	numberOfTeams = 31	
	year = int(year)
	if(year >= 2018):
		numberOfTeams = 31
	elif(year >= 2000 and year < 2017):
		numberOfTeams = 30
	elif(year >= 1999 and year < 2000):
		numberOfTeams = 28
	elif(year >= 1998 and year < 1999):
		numberOfTeams = 27
	elif(year >= 1993 and year < 1998):
		numberOfTeams = 26
	elif(year >= 1992 and year < 1993):
		numberOfTeams = 24
	elif(year >= 1991 and year < 1992):
		numberOfTeams = 22
	elif(year >= 1979 and year < 1991):
		numberOfTeams = 21
	elif(year >= 1978 and year < 1979):
		numberOfTeams = 17
	elif(year >= 1974 and year < 1978):
		numberOfTeams = 18
	elif(year >= 1972 and year < 1974):
		numberOfTeams = 16
	elif(year >= 1970 and year < 1972):
		numberOfTeams = 14
	elif(year >= 1967 and year < 1970):
		numberOfTeams = 12
	elif(year >= 1942 and year < 1967):
		numberOfTeams = 6
	

	# Determine which year due to fluctuations in number of draft rounds
	if(year >= 2005):
		numberOfRounds = 7
	elif(year >= 1995 and year < 2005):
		numberOfRounds = 9
	elif(year >= 1992 and year < 1995):
		numberOfRounds = 11
	elif(year >= 1981 and year < 1992):
		numberOfRounds = 12

	isCurrentTeam = False
	
	season_URL = main_api + teams + "?season=" + str(year) + str(year + 1)
	season_json_data = requests.get(season_URL).json()

	for team in range(0, numberOfTeams):
		teamID = season_json_data["teams"][team]["id"]		
		if(str(teamID) == team_api_id):
			isCurrentTeam = True
			break
		else:
			isCurrentTeam = False

	if(isCurrentTeam):
		# Print all players in each round for selected team
		for draftRound in range(0, numberOfRounds):
			for draftPick in range(0, numberOfTeams):
				if(str(shortenedSearch[0]["rounds"][draftRound]["picks"][draftPick]["team"]["id"]) == str(team_api_id)):
					player = shortenedSearch[0]["rounds"][draftRound]["picks"][draftPick]["prospect"]["fullName"]
					draftPickOverall = str(shortenedSearch[0]["rounds"][draftRound]["picks"][draftPick]["pickOverall"])
				
					careerRegularSeasonStatsLink = "/stats?stats=careerRegularSeason"
					careerPlayoffsStatsLink = "/stats?stats=careerPlayoffs"

					# Get player position
					playerLink = shortenedSearch[0]["rounds"][draftRound]["picks"][draftPick]["prospect"]["link"]
					json_data = requests.get(short_api + playerLink).json()
					
					# Add th nd st to overall draft position
					try: 
						if(draftPickOverall[-1] == "1"):
							draftPickOverall = draftPickOverall + "st"
						elif(draftPickOverall[-1] == "2" or draftPickOverall[-1] == "3"):
							draftPickOverall = draftPickOverall + "nd"
						else:
							draftPickOverall = draftPickOverall + "th"

						position = json_data["prospects"][0]["primaryPosition"]["abbreviation"]

						# Print player and position if data available
						print(player + " " + position)
					except:
						# Not available, only print player
						print(player)
					
				
					print("Round: " + str(draftRound + 1) + " | Draft Pick: " + str(draftPick + 1))
					print("Overall: " + draftPickOverall)
					print()
	else:
		print()
		print("There is no data for the team in the selected year")

# Get draft year of team then return players, draft position, position (if applicable),
# draft round and overall selection 
def getDraft(link):
	year = input("Please enter a draft year: ")
	draft = "/draft/" + year
	parseUrl = main_api + draft
	json_data = requests.get(parseUrl).json()
	shortenedSearch = json_data["drafts"]

	# Adjust number of teams depending on what year is queried
	numberOfTeams = 31	
	year = int(year)
	if(year >= 2018):
		numberOfTeams = 31
	elif(year >= 2000 and year < 2017):
		numberOfTeams = 30
	elif(year >= 1999 and year < 2000):
		numberOfTeams = 28
	elif(year >= 1998 and year < 1999):
		numberOfTeams = 27
	elif(year >= 1993 and year < 1998):
		numberOfTeams = 26
	elif(year >= 1992 and year < 1993):
		numberOfTeams = 24
	elif(year >= 1991 and year < 1992):
		numberOfTeams = 22
	elif(year >= 1979 and year < 1991):
		numberOfTeams = 21
	elif(year >= 1978 and year < 1979):
		numberOfTeams = 17
	elif(year >= 1974 and year < 1978):
		numberOfTeams = 18
	elif(year >= 1972 and year < 1974):
		numberOfTeams = 16
	elif(year >= 1970 and year < 1972):
		numberOfTeams = 14
	elif(year >= 1967 and year < 1970):
		numberOfTeams = 12
	elif(year >= 1942 and year < 1967):
		numberOfTeams = 6
	

	# Determine which year due to fluctuations in number of draft rounds
	if(year >= 2005):
		numberOfRounds = 7
	elif(year >= 1995 and year < 2005):
		numberOfRounds = 9
	elif(year >= 1992 and year < 1995):
		numberOfRounds = 11
	elif(year >= 1981 and year < 1992):
		numberOfRounds = 12

	isCurrentTeam = False
	draftHistoryOutput = ''
	
	season_URL = main_api + teams + "?season=" + str(year) + str(year + 1)
	season_json_data = requests.get(season_URL).json()

	for team in range(0, numberOfTeams):
		teamID = season_json_data["teams"][team]["id"]		
		if(str(teamID) == team_api_id):
			isCurrentTeam = True
			break
		else:
			isCurrentTeam = False

	if(isCurrentTeam):
		# Print all players in each round for selected team
		for draftRound in range(0, numberOfRounds):
			for draftPick in range(0, numberOfTeams):
				if(str(shortenedSearch[0]["rounds"][draftRound]["picks"][draftPick]["team"]["id"]) == str(team_api_id)):
					player = shortenedSearch[0]["rounds"][draftRound]["picks"][draftPick]["prospect"]["fullName"]
					draftPickOverall = str(shortenedSearch[0]["rounds"][draftRound]["picks"][draftPick]["pickOverall"])
				
					careerRegularSeasonStatsLink = "/stats?stats=careerRegularSeason"
					careerPlayoffsStatsLink = "/stats?stats=careerPlayoffs"

					# Get player position
					playerLink = shortenedSearch[0]["rounds"][draftRound]["picks"][draftPick]["prospect"]["link"]
					json_data = requests.get(short_api + playerLink).json()
					
					# Add th nd st to overall draft position
					try: 
						if(draftPickOverall[-1] == "1"):
							draftPickOverall = draftPickOverall + "st"
						elif(draftPickOverall[-1] == "2" or draftPickOverall[-1] == "3"):
							draftPickOverall = draftPickOverall + "nd"
						else:
							draftPickOverall = draftPickOverall + "th"

						position = json_data["prospects"][0]["primaryPosition"]["abbreviation"]

						# Print player and position if data available
						# print(player + " " + position)

						draftHistoryOutput += "{}, {}\n".format(player, position)
					except:
						# Not available, only print player
						# print(player)
						draftHistoryOutput += player + "\n"
					
					draftHistoryOutput += "Round: {} | Draft Pick: {}\n".format(str(draftRound + 1), str(draftPick + 1))
					draftHistoryOutput += "Overall: {}\n".format(draftPickOverall)
					draftHistoryOutput += "\n"
				
		print(draftHistoryOutput)
		
	else:
		print()
		print("There is no data for the team in the selected year")
	
	return draftHistoryOutput

# Print next game for selected team
def getNextGame(link):
	parsedData = urlParser(link, nextGame)
	shortenedSearch = parsedData["teams"]
	awayTeam = shortenedSearch[0]["nextGameSchedule"]["dates"][0]["games"][0]["teams"]["away"]["team"]["name"]
	homeTeam = shortenedSearch[0]["nextGameSchedule"]["dates"][0]["games"][0]["teams"]["home"]["team"]["name"]

	# Print team names and team scores
	nextGameOutput = ""
	nextGameOutput += "\nNext Game\n"
	nextGameOutput += "{} at {}".format(awayTeam, homeTeam)

	print(nextGameOutput)

	return nextGameOutput

# Print previous game for selected team
def getPreviousGame(link):
	parsedData = urlParser(link, previousGame)
	shortenedSearch = parsedData["teams"]	
	awayTeam = shortenedSearch[0]["previousGameSchedule"]["dates"][0]["games"][0]["teams"]["away"]["team"]["name"]
	homeTeam = shortenedSearch[0]["previousGameSchedule"]["dates"][0]["games"][0]["teams"]["home"]["team"]["name"]
	awayScore = shortenedSearch[0]["previousGameSchedule"]["dates"][0]["games"][0]["teams"]["away"]["score"]
	homeScore = shortenedSearch[0]["previousGameSchedule"]["dates"][0]["games"][0]["teams"]["home"]["score"]

	# Print team names and team scores
	previousGameOutput = ""
	previousGameOutput += "\nPrevious Game\n"
	previousGameOutput += "{}: {} | {}: {}".format(awayTeam, str(awayScore), homeTeam, str(homeScore))

	print(previousGameOutput)

	return previousGameOutput

# Print divisional standigns for selected team using current date
def getRegularSeasonStandings(link):
	parsedData = main_api + regularSeason
	json_data = requests.get(parsedData).json()
	numDivisionTeams = 0

	# Loop through all divisions, determine division team is in, then print division standings
	for i in range(0, 4):
		numDivisionTeams = len(json_data["records"][i]["teamRecords"])
		for j in range(0, numDivisionTeams):
			if(json_data["records"][i]["teamRecords"][j]["team"]["link"] == link):
				divisionID = json_data["records"][i]["division"]["id"]
				# Metropolitan - 18
				if(divisionID == 18):
					arrayDivisionID = 0
					break
				# Atlantic - 17
				elif(divisionID == 17):
					arrayDivisionID = 1
					break
				# Central - 16
				elif(divisionID == 16):
					arrayDivisionID = 2
					break
				# Pacific - 15
				elif(divisionID == 15):
					arrayDivisionID = 3
					break

	# Loop through division and print each team in the standings
	teamNameStandingsOutput = ""
	for team in range(0, numDivisionTeams):
		teamNameStandingsOutput += "\n%s. %s" % ((str(team + 1)), (json_data["records"][arrayDivisionID]["teamRecords"][team]["team"]["name"]))

	print(teamNameStandingsOutput)

	return teamNameStandingsOutput


####################### HELPER FUNCTIONS #######################
# Print position and name of players
def printPosition(position, printPosition):
	if(printPosition == "Goalie"):
		print("Goalie: ")
	elif(printPosition == "Center"):
		print("Center: ")
	elif(printPosition == "Left Wing"):
		print("Left Wing: ")
	elif(printPosition == "Right Wing"):
		print("Right Wing: ")
	elif(printPosition == "Defenseman"):
		print("Defensemen: ")

	for player in position:
		print(player)
	print()

# Print number and player name
def appendNamesAndNumber(position, rosterData, index):
	position.append(rosterData[index]["jerseyNumber"] + " " + rosterData[index]["person"]["fullName"])

# Parse urls with and return appropriate JSON data
def urlParser(link, userSelection):
	parseUrl = short_api + link + userSelection
	json_data = requests.get(parseUrl).json()
	return json_data

# Get NHL defined team API ID for selected team
def getTeamAPIID(teamName):
	parseUrl = main_api + teams
	json_data = requests.get(parseUrl).json()
	global team_api_id
	
	for team in json_data["teams"]:
		if team['name'] == teamName:
			team_api_id = str(team['id'])

# Get team names in list
def getTeamList(json_data):
	print("Please type the number associated with a team to view more information\n")
	for item in json_data["teams"]:
		teamsList.append(item["name"])

# UI divider
def divider():
	print()
	print("\n*********************************************************************")
	print()

def clearVariables():
	global team_api_id 
	team_api_id = ""

	global team
	team = ""

	global link
	link = ""

	global teamsList
	teamsList = []


####################### MAIN #######################
# Create URL
def startProgram():
	clearVariables()
	url = main_api + teams
	json_data = requests.get(url).json()

	# Load team names in list
	getTeamList(json_data)

	# Sort alphabetically
	teamsList.sort()

	printTeams()
	link = userTeamInput(json_data)
	viewMoreInformation(link)

isContinue = True

while(isContinue == True):
	startProgram()

	print()
	userInput = str(input("Type R to restart or Q to quit: "))
	if(userInput.upper() == "R"):
		isContinue = True
	elif(userInput.upper() == "Q"):
		isContinue = False
		divider()
		print("Goodbye")




