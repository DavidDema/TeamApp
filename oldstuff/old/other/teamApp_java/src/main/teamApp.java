package main;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import competition.Competition;
import competition.Cup;
import competition.League;
import competition.Team;
import competition.event.Event;
import competition.event.Game;
import competition.event.Training;
import dataStream.InputData;
import dataStream.ics;
import user.User;
import user.subuser.Player;
import user.subuser.Trainer;

public class teamApp {
	
	public static List<User> users = new ArrayList<User>();
	public static List<Player> players = new ArrayList<Player>();
	public static List<Trainer> trainers = new ArrayList<Trainer>();
	
	public static List<Team> teams = new ArrayList<Team>();
	
	public static List<Event> events = new ArrayList<Event>();
	public static List<Game> games = new ArrayList<Game>();
	public static List<Training> training = new ArrayList<Training>();
	
	public static List<Competition> competitions = new ArrayList<Competition>();
	public static List<League> leagues = new ArrayList<League>();
	public static List<Cup> cups = new ArrayList<Cup>();
	
	public teamApp() {
		
	}
	
	public static Team getTeam(String teamName) {
		for(int i=0;i<teamApp.teams.size();i++) {
			if(teamApp.teams.get(i).name.equals(teamName))
				return teamApp.teams.get(i);
		}
		System.out.println("Error:" + teamName);
		return null;
	}
	
	public static Competition getCompetition(String competitionName) {
		for(int i=0;i<teamApp.competitions.size();i++) {
			if(teamApp.competitions.get(i).name.equals(competitionName))
				return teamApp.competitions.get(i);
		}
		System.out.println("Error:" + competitionName);
		return null;
	}
	
	public static Team getTeam(int ID) {
		//TODO
		return null;
	}
	
	public static Event getEvent(String eventName) {
		for(int i=0;i<teamApp.events.size();i++) {
			if(teamApp.events.get(i).name.equals(eventName))
				return teamApp.events.get(i);
		}
		return null;
	}
	
	public static Game getGame(int ID) {
		//TODO
		return null;
	}
	
	
	//----------------------------------------------
	//----------------------------------------------
	public static void addUsersCSV(String filename) {
		
		List<String> input = InputData.processInputFile(filename,1);
		
		teamApp.addUser(input.stream().map((line) -> {
			return new User(teamApp.users.size(), line, true);
		}).collect(Collectors.toList()));
		
		//return true
	}
	
	public static void addPlayersCSV(String filename) {
		
		List<String> input = InputData.processInputFile(filename,1);
		teamApp.addPlayer(input.stream().map((line) -> {
			return new Player(teamApp.players.size(), line,false);
		}).collect(Collectors.toList()));
		
		//return true
	}

	public static void addTeamsCSV(String filename) {
		
		List<String> input = InputData.processInputFile(filename,1);
		
		teamApp.addTeam(input.stream().map((line) -> {
			return new Team(teamApp.teams.size(),line, false);
			//TODO add comp
		}).collect(Collectors.toList()));
	}
	
	public static void addEventsCSV(String filename) {
		
		List<String> input = InputData.processInputFile(filename,1);
		
		teamApp.addEvent(input.stream().map((line) -> {
			return new Event(teamApp.events.size(),line);
		}).collect(Collectors.toList()));
	}
	
	public static void addGamesICS(List<String> list) {
		//Order: 0"BEGIN:", 1"DTSTAMP:", 2"DTSTART:", 3"DURATION:", 4"SUMMARY:", 5"DESCRIPTION:",
		//6"UID:", 7"X-HOMENR:", 8"X-AWAYNR", 9"URL:", 10"LOCATION:", 11"END:"
		if(list.size()>=13)
			System.out.print("Error ICS");
		//System.out.print(list);
		
		String tname = list.get(0);
		String tdate = list.get(2);
		String tduration = list.get(3);
		String tsummary = list.get(4);
		String tdescription = list.get(5);
		String turl = list.get(9);
		String tplace = list.get(10);
		
		
		//20200919T140000Z
		DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd'T'HHmmss'Z'");
		LocalDateTime date = LocalDateTime.parse(tdate,formatter);
		
		String name = tname;
		int duration = 0;
		String place = tplace;
		
		
		
		
		List<String> comp_round = ics.getCompetitionText(tdescription);
		
		Competition comp = teamApp.getCompetition(comp_round.get(0));
		int round = Integer.parseInt(comp_round.get(1));
		
		//System.out.print(tsummary);
		List<String> teams = ics.getTeamText(tsummary);
		Team homeTeam = teamApp.getTeam(teams.get(0));
		Team awayTeam = teamApp.getTeam(teams.get(1));
		
		
		if(homeTeam!=null&&awayTeam!=null)
			teamApp.addGame(new Game(teamApp.teams.size(), name, date, place, duration, homeTeam, awayTeam, comp));
	}
	
	//------------------------------------------------
	public static boolean addCompetition(Competition competition) {
		if(teamApp.competitions.contains(competition))
			return false;
		if(!teamApp.competitions.add(competition))
			return false;
		return true;

	}
	public static boolean addCompetition(List<Competition> competition) {
		if(teamApp.competitions.containsAll(competition))
			return false;
		if(!teamApp.competitions.addAll(competition))
			return false;
		return true;
	}
	public static boolean removeCompetition(Competition competition) {
		if(teamApp.competitions.contains(competition))
			return false;
		if(!teamApp.competitions.remove(competition))
			return false;
		return true;

	}
	public static boolean removeCompetition(List<Competition> competition) {
		if(teamApp.competitions.containsAll(competition))
			return false;
		if(!teamApp.competitions.removeAll(competition))
			return false;
		return true;
	}
	//------------------------------------------------
	public static boolean addPlayer(Player player) {
		if(teamApp.players.contains(player))
			return false;
		if(!teamApp.players.add(player))
			return false;
		return true;

	}
	public static boolean addPlayer(List<Player> player) {
		if(teamApp.players.containsAll(player))
			return false;
		if(!teamApp.players.addAll(player))
			return false;
		return true;
	}
	public static boolean removePlayer(Player player) {
		if(teamApp.players.contains(player))
			return false;
		if(!teamApp.players.remove(player))
			return false;
		return true;

	}
	public static boolean removePlayer(List<Player> player) {
		if(teamApp.players.containsAll(player))
			return false;
		if(!teamApp.players.removeAll(player))
			return false;
		return true;
	}
	//------------------------------------------------
	public static boolean addUser(User user) {
		if(teamApp.users.contains(user))
			return false;
		if(!teamApp.users.add(user))
			return false;
		return true;

	}
	public static boolean addUser(List<User> user) {
		if(teamApp.users.containsAll(user))
			return false;
		if(!teamApp.users.addAll(user))
			return false;
		return true;
	}
	public static boolean removeUser(User user) {
		if(teamApp.users.contains(user))
			return false;
		if(!teamApp.users.remove(user))
			return false;
		return true;

	}
	public static boolean removeUser(List<User> user) {
		if(teamApp.users.containsAll(user))
			return false;
		if(!teamApp.users.removeAll(user))
			return false;
		return true;
	}
	//-------------------------------------------------
	public static boolean addGame(Game game) {
		if(teamApp.games.contains(game))
			return false;
		if(!teamApp.games.add(game))
			return false;
		return true;

	}
	public static boolean addGame(List<Game> game) {
		if(teamApp.games.containsAll(game))
			return false;
		if(!teamApp.games.addAll(game))
			return false;
		return true;
	}
	public static boolean removeGame(Game game) {
		if(teamApp.games.contains(game))
			return false;
		if(!teamApp.games.remove(game))
			return false;
		return true;

	}
	public static boolean removeGame(List<Game> game) {
		if(teamApp.games.containsAll(game))
			return false;
		if(!teamApp.games.removeAll(game))
			return false;
		return true;
	}
	//-------------------------------------------------
	public static boolean addEvent(Event event) {
		if(teamApp.events.contains(event))
			return false;
		if(!teamApp.events.add(event))
			return false;
		return true;

	}
	public static boolean addEvent(List<Event> event) {
		if(teamApp.events.containsAll(event))
			return false;
		if(!teamApp.events.addAll(event))
			return false;
		return true;
	}
	public static boolean removeEvent(Event event) {
		if(teamApp.events.contains(event))
			return false;
		if(!teamApp.events.remove(event))
			return false;
		return true;

	}
	public static boolean removeEvent(List<Event> event) {
		if(teamApp.events.containsAll(event))
			return false;
		if(!teamApp.events.removeAll(event))
			return false;
		return true;
	}
	//-------------------------------------------------
	public static boolean addTeam(Team team) {
		if(teamApp.teams.contains(team))
			return false;
		if(!teamApp.teams.add(team))
			return false;
		return true;

	}
	public static boolean addTeam(List<Team> team) {
		if(teamApp.teams.containsAll(team))
			return false;
		if(!teamApp.teams.addAll(team))
			return false;
		return true;
	}
	public static boolean removeTeam(Team team) {
		if(teamApp.teams.contains(team))
			return false;
		if(!teamApp.teams.remove(team))
			return false;
		return true;

	}
	public static boolean removeTeam(List<Team> team) {
		if(teamApp.teams.containsAll(team))
			return false;
		if(!teamApp.teams.removeAll(team))
			return false;
		return true;
	}
}
