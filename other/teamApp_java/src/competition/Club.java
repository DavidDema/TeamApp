package competition;

import java.util.ArrayList;

import competition.event.Event;
import user.User;

public class Club {

	public ArrayList<Team> teams = new ArrayList<Team>();
	public String name;
	public ArrayList<Competition> competitions = new ArrayList<Competition>();
	
	public User obmann;
	public ArrayList<Event> events = new ArrayList<Event>();
	
	public Club(String name) {
		this.name = name;
	}
	
	public boolean addTeam(Team team){
		if(this.teams.contains(team))
			return false;
		this.teams.add(team);
		return true;
	}
	
	public boolean addTeams(ArrayList<Team> teams){
		if(this.teams.containsAll(teams))
			return false;
		this.teams.addAll(teams);
		return true;
		//TODO what if one team from list is in this team list
	}
	
	public String toString() {
		String summary = "";
		summary += 
				"Club name:" + this.name +
				"Competition:" + this.competitions;
		return summary;
	}
}