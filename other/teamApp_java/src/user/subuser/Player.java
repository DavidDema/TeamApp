package user.subuser;
import java.util.ArrayList;

import competition.Team;
import competition.event.Event;
import main.teamApp;
import user.User;

public class Player extends User {

	public Team team;
	
	//statistics
	public int shirtNumber;
	public float rating;
	public String foot;
	public boolean inLineup;
	public Position position;
	public int yellowCards;
	public int redCards;
	public int goals;
	public int assists;
	public int gamesPlayed;
	public int minutesPlayed;
	public float minutesAverage;	

	public Player(int user_id, String input, boolean print) {
		super(user_id, input, true);
		
		String[] p = input.split(",");// a CSV has comma separated lines
		
		String team = p[1];
		  
		this.addTeam(teamApp.getTeam(team));
		
		if(print)
			System.out.print("New Player added:\n"+this);
	}
	
	public boolean addTeam(Team team) {
		this.team = team;
		return this.team.addPlayer(this);
	}
	
	public Position getPos() {
		// TODO - implement Player.getPos
		throw new UnsupportedOperationException();
	}
	
	
	public boolean inLineup(int game, int starting) {
		// TODO - implement Player.inLineup
		throw new UnsupportedOperationException();
	}
	
	public boolean setTeam(Team team) {
		
		this.team = team;
		this.team.addPlayer(this);
		
		return true;
	}
	
	public void addCard(String color) {
			
		if(color=="red"||color=="RED"||color=="Red") {
			this.redCards ++;
		}
		if(color=="yellow"||color=="YELLOW"||color=="Yellow") {
			this.yellowCards ++;
		}
	}
	
	public void goal() {
		
		this.goals ++;
	}
	
	public void clearGoals() {
		
		this.goals = 0;
	}
	
	public void setPosition(String position) {
		this.position = Position.valueOf(position);
	}
	
	public String toString() {
		String summary = "";
		summary += 
				this.id +"Player name:" + super.name + "\n" +
				"Team:" + this.team.name + "\n";
				//"Age:" + super.age + "\n" +
				//"Position:" + this.position.toString() + "\n";
		
		return summary;
	}
	
	public static boolean addPlayers(ArrayList<Player> players2) {
		return false;
	}

}