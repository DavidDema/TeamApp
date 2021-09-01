package competition;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import competition.*;
import competition.event.Game;
import competition.event.Event;
import competition.event.Training;
import dataStream.InputData;
import user.subuser.Player;

public class Team {

	public int id;
	public String name;
	public int picture;
	
	public Club club;
	public List<Competition> competitions = new ArrayList<Competition>();
	
	public ArrayList<Player> players = new ArrayList<Player>();
	public ArrayList<Game> games = new ArrayList<Game>();
	public List<Training> trainings = new ArrayList<Training>();
	
	public int points;

	public Team(int team_id, String input, boolean print) {
		String[] t = input.split(",");// a CSV has comma separated lines
		
		//this.competitions.add(comp);
		
		this.name = t[0];
		
		if(print)
			System.out.print("New Team added:\n"+this);
	}
	
	public ArrayList<Player> getPlayers() {
		return this.players;
	}
	
	public boolean addCompetition(Competition competition) {
		if(this.competitions.contains(competition))
			return false;
		this.competitions.add(competition);
		return competition.addTeam(this);
	}
	
	public boolean addGame(Game game) {
		if(this.games.contains(game))
			return false;
		this.games.add(game);
		return true;
	}
	
	public boolean addPlayer(Player player) {
		if(this.players.contains(player))
			return false;
		this.players.add(player);
		return true;
	}
	
	public boolean addPlayer(List<Player> players) {
		//TODO check if one object is already in list
		if(this.players.containsAll(players))
			return false;
		this.players.addAll(players);
		return true;
	}
	
	public boolean removePlayer(Player player) {
		if(!this.players.contains(player))
			return false;
		this.players.remove(player);
		return true;
	}
	
	public boolean removePlayer(List<Player> players) {
		//TODO check if one object is already in list
		if(!this.players.containsAll(players))
			return false;
		this.players.removeAll(players);
		return true;
	}
	
	public boolean setNominatedPlayers(Game game, List<Player> players) {
		if(this.games.contains(game))
			return game.addNominatedPlayer(players);
		return false;
	}
	
	public boolean setLineupPlayers(Game game, List<Player> players) {
		if(this.games.contains(game))
			return game.addLineupPlayer(players);
		return false;
	}
	
	public boolean setPicture(String filename) {
		//TODO
		return false;
	}
	
	public String toString() {
		String summary = "";
		summary += 
				"Team name:" + this.name + "\n" +
				"Players:" + this.players.size() + "\n";
		for(int i=0;i<this.players.size();i++) {
			summary +=
				this.players.get(i).name + "\n";
		}
		return summary;
	}
	
	public Player getPlayer(String playerName) {
		for(int i=0;i<this.players.size();i++) {
			if(this.players.get(i).name == playerName)
				return this.players.get(i);
		}
		return null;
	}
	
}