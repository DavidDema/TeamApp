package competition.event;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import competition.Competition;
import competition.PitchType;
import competition.Team;
import main.teamApp;
import user.User;
import user.subuser.Player;

public class Game extends Event {

	public PitchType pitchType;
	public GameState state;
	public Competition competition;
	public int round;
	
	public Team winner;
	public Team homeTeam;
	public Team awayTeam;
	
	public List<Player> ht_missingPlayers = new ArrayList<Player>(); //players not nominated
	public List<Player> ht_nominatedPlayers = new ArrayList<Player>(); //players nominated for match
	public List<Player> ht_lineupPlayers = new ArrayList<Player>(); //players in line-up
	
	public List<Player> at_missingPlayers = new ArrayList<Player>(); //players not nominated
	public List<Player> at_nominatedPlayers = new ArrayList<Player>(); //players nominated for match
	public List<Player> at_lineupPlayers = new ArrayList<Player>(); //players in line-up
	
	public int ht_goals;
	public int at_goals;
	public int ht_redCards;
	public int ht_yellowCards;
	public int at_redCards;
	public int at_yellowCards;
	
	public Game(int event_id, String name, LocalDateTime date, String place, int duration, Team homeTeam, Team awayTeam, Competition comp){
		super(event_id, name,date,place,duration);
		
		this.competition = comp;
		
		this.homeTeam = homeTeam;
		this.awayTeam = awayTeam;
		
		this.state = GameState.NOTSTARTED;
		
		System.out.print("New Game added:\n"+this+"\n");
	}
	
	public Game(int event_id, String input){
		super(event_id, input);
		
		String[] g = input.split(",");// a CSV has comma separated lines
		
		this.competition = null;
		
		this.homeTeam = teamApp.getTeam(g[0]);
		this.awayTeam = teamApp.getTeam(g[1]);
		this.date = LocalDateTime.now();
		this.round = 1;
		this.state = this.update();
	}
	
	public boolean addCompetition(Competition competition) {
		this.competition = competition;
		this.competition.addGame(this);
		return true;
	}
	
	public boolean addTeams(Team ht, Team at) {
		this.homeTeam = ht;
		this.awayTeam = at;
		this.homeTeam.addGame(this);
		this.awayTeam.addGame(this);
		return true;
	}
	
	public GameState update() {
		//TODO
		return GameState.NOTSTARTED;
	}
	
	public boolean setGoal(Team team, Player player) {
		
		switch(this.isTeam(team)) {
		case 1:
			this.ht_goals++;
			break;
		case 2:	
			this.at_goals++;
			break;
		case 0:
			return false;
		default:
			return false;
		}
		player.goal();
		return true;
	}
	
	public boolean undoGoal(Team team) {
		switch(this.isTeam(team)) {
		case 1:
			if(ht_goals>0)
				this.ht_goals--;
			break;
		case 2:
			if(at_goals>0)
				this.at_goals--;
			break;
		case 0:
			return false;
		default:
			return false;
		}
		return true;
	}

	public Team getHomeTeam() {
		return this.homeTeam;
	}
	
	public Team getAwayTeam() {
		return this.awayTeam;
	}
	
	public boolean setWin(Team winnerTeam) {
		if(this.winner==null) {
			if(this.isTeam(winnerTeam)==0) {
				System.out.println("cannot set winner Team: team not in game");
				return false;
			}
			
			this.winner = winnerTeam;
			this.state = GameState.FINISHED;
			return true;
		}else {
			System.out.println("cannot set winner Team: winner has been defined already, please use undoWin()");
			return false;
		}
	}

	public boolean undoWin() {
		if(this.winner!=null) {
			this.winner = null;
			//TODO this.state = GameState.RUNNING ? evtl als parameter
			return true;
		}else {
			return true;
		}
	}
	
	public boolean setStatus(GameState gameState) {
		//TODO check if game started to finish etc
		this.state = gameState;
		//this.update();
		return true;
	}
	
	public boolean setStatus(String gameState) {
		//TODO check if game started to finish etc
		this.state = GameState.valueOf(gameState);
		//this.update();
		return true;
	}
	
	public boolean isStarted() {
		if(this.state==GameState.RUNNING)
			return true;
		return false;
	}
	
	public boolean setRedCard(Team team, Player player) {
		
		if(this.isTeam(team)!=0) {
			if(team.players.contains(player)) {
				player.addCard("Red");
				//players on field -1
				//this.playersOnPitch(11, 10)
				return true;
			}else {
				System.out.print("Cannot give Red Card to Player: Not in selected team");
				return false;
			}
		}else
			System.out.print("Cannot give Red Card to Player: Not in one of the teams");
			return false;
	}

	public boolean setYellowCard(Team team, Player player) {
		
		if(this.isTeam(team)!=0) {
			if(team.players.contains(player)) {
				player.addCard("Yellow");
				return true;
			}else {
				System.out.print("Cannot give Yellow Card to Player: Not in selected team");
				return false;
			}
		}else {
			System.out.print("Cannot give Yellow Card to Player: Not in one of the teams");
			return false;
		}
	}
	
	public boolean addNominatedPlayer(Player player) {
		//if(!this.isPart(players))
			//return false;
		switch(this.isPlayer(player)) {
			case 1:
				this.ht_nominatedPlayers.add(player);
				break;
			case 2:
				this.ht_nominatedPlayers.add(player);
				break;
			case 0:
				return false;
			default:
				return false;
		}
		return true;
	}
	
	public boolean addNominatedPlayer(List<Player> players) {
		//if(!this.isPart(players))
			//return false;
		switch(this.isPlayer(players)) {
			case 1:
				this.ht_nominatedPlayers = players;
				break;
			case 2:
				this.ht_nominatedPlayers = players;
				break;
			case 0:
				return false;
			default:
				return false;
		}
		return true;
	}
	
	public boolean addLineupPlayer(Player player) {
		//if(!this.isPart(players))
			//return false;
		switch(this.isPlayer(player)) {
			case 1:
				this.ht_lineupPlayers.add(player);
				break;
			case 2:
				this.at_lineupPlayers.add(player);
				break;
			case 0:
				return false;
			default:
				return false;
		}
		return true;
	}
	
	public boolean addLineupPlayer(List<Player> players) {
		//if(!this.isPart(players))
			//return false;
		switch(this.isPlayer(players)) {
			case 1:
				this.ht_lineupPlayers = players;
				break;
			case 2:
				this.at_lineupPlayers = players;
				break;
			case 0:
				return false;
			default:
				return false;
		}
		return true;
	}
	
	
	public void clearPlayers() {
		this.ht_lineupPlayers = null;
		this.ht_missingPlayers = null;
		this.ht_nominatedPlayers = null;
		
		this.at_lineupPlayers = null;
		this.at_missingPlayers = null;
		this.at_nominatedPlayers = null;
	}
	
	public int isPlayer(Player player) {
		
		if(this.homeTeam.players.contains(player))
			return 1;
		if(this.awayTeam.players.contains(player))
			return 2;
		return 0;
	}
	
	public int isPlayer(List<Player> players) {

		if(this.homeTeam.players.containsAll(players))
			return 1;
		if(this.awayTeam.players.containsAll(players))
			return 2;
		return 0;
	}
	
	public int isTeam(Team team) {
		
		if(this.homeTeam.equals(team))
			return 1;
		if(this.awayTeam.equals(team))
			return 2;
		return 0;
	}
	
	public String toString() {
		String summary = "";
		summary += 
				this.homeTeam.name + " : " +  this.awayTeam.name + "\n" +
				"Date:" + super.date.toString();
		return summary;
	}

}