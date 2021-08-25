package competition.event;
import java.time.LocalDateTime;
import java.util.ArrayList;

import competition.Club;
import competition.PitchType;
import competition.Team;

public class Training extends Event {

	public PitchType pitchType;
	public ArrayList<Team> teams = new ArrayList<Team>();
	public Club club;
	
	public Training(int event_id, String name, LocalDateTime date, String place, int duration){
		super(event_id, name, date, place, duration);
	}
	
	public boolean addTeam(Team team) {
		if(this.teams.contains(team))
			return false;
		this.teams.add(team);
		return true;
	}
	
	public boolean addClub(Club club) {
		if(this.teams.containsAll(club.teams))
			return false;
		this.teams.addAll(club.teams);
		return true;
	}
}