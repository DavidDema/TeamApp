package competition;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import competition.event.Game;
import dataStream.InputData;
import dataStream.ics;
import user.subuser.Player;

public class Competition {

	public int id;
	public String name;
	public String nation;
	public String city;
	public ArrayList<Team> teams = new ArrayList<Team>();
	public ArrayList<Game> games = new ArrayList<Game>();
	
	public Competition(int comp_id, String name) {
		this.id = comp_id;
		this.name = name;
		
		System.out.print("Competition added:\n" +this+ "\n");
	}
	
	public boolean addTeam(Team team) {
		if(this.teams.contains(team))
			return false;
		return this.teams.add(team);
	}
	
	public boolean addTeam(List<Team> teams) {
		//TODO check if teams already in list
		if(this.teams.containsAll(teams))
			return false;
		return this.teams.addAll(teams);
	}
	
	public boolean removeTeam(Team team) {
		if(!this.teams.contains(team))
			return false;
		return this.teams.remove(team);
	}
	
	public boolean removeTeam(List<Team> teams) {
		//TODO check if teams already in list
		if(!this.teams.containsAll(teams))
			return false;
		return this.teams.removeAll(teams);
	}
	
	public boolean addGame(Game game) {
		if(this.games.contains(game))
			return false;
		return this.games.add(game);
	}
	
	public boolean addGames(List<Game> games) {
		//TODO check if games already in list
		if(this.games.containsAll(games))
			return false;
		this.games.addAll(games);
		return true;
	}
	
	public boolean removeGame(Game game) {
		if(!this.games.contains(game))
			return false;
		this.games.remove(game);
		return true;
	}
	
	public boolean removeGames(List<Game> games) {
		//TODO check if games already in list
		if(!this.games.containsAll(games))
			return false;
		this.games.removeAll(games);
		return true;
	}
	
	public String toString() {
		String summary = "";
		summary += 
				"Competition name:" + this.name + "\n" +
				"Teams:" + this.teams.size() + "\n";
		for(int i=0;i<this.teams.size();i++) {
			summary +=
				this.teams.get(i).name + "\n";
		}
		summary += "Games:" + this.games.size() + "\n";
		for(int i=0;i<this.games.size();i++) {
			summary +=
				this.games.get(i) + "\n";
		}
		return summary;
	}
}