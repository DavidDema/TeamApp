package competition.event;
import java.time.*;
import java.util.ArrayList;
import java.util.List;

import user.User;

public class Event {

	public int id;
	public String name;
	public String description;
	public EventState state;
	public boolean acitve;
	
	public List<User> invited = new ArrayList<User>();
	public List<User> participants = new ArrayList<User>();
	public List<User> notPart = new ArrayList<User>();
	
	
	public LocalDateTime date;
	public int duration; //minutes
	
	public String place;
	public String placeLink;
	
	public Event followingEvent;
	
	
	
	public Event(int event_id, String name, LocalDateTime date, String place, int duration){
		this.id = event_id;
		
		this.name = name;
		this.date = date;
		this.place = place;
		this.duration = duration;
		this.state = EventState.SUGGESTED;
	}
	
	public Event(int event_id, String input) {
		this.id = event_id;
		
		String[] g = input.split(",");// a CSV has comma separated lines

		this.name = "Test1";
		this.date = LocalDateTime.parse(g[2]);
	}
	
	public boolean hasFollowingEvent() {
		if(this.followingEvent==null)
			return false;
		return true;
	}
	
	public void changeDuration(int newDuration) {
		this.duration = newDuration;
	}
	
	public boolean changeDate(LocalDateTime newDate) {
		this.date = newDate;
		return true;
	}
	
	public boolean changeTime(LocalDate time) {
		// TODO - implement Game.undoGoal
	    throw new UnsupportedOperationException();
	}
	
	
//--------------------------
	
	public boolean addResponse(User user, boolean response) {
		if(!this.isInvited(user)) {
			System.out.print("User not invited to Event");
			return false;
		}
		if(this.isPart(user))
			//TODO: update response OK
		
		if(response) {
			this.participants.add(user);
		}else {
			this.notPart.add(user);
		}
		return true;
	}
	
	public boolean isInvited(User user) {
		if(this.invited.contains(user))
			return true;
		return false;
	}
	public boolean isInvited(List<User> users) {
		if(this.invited.containsAll(users))
			return true;
		return false;
	}
	
	public boolean isPart(User user) {
		if(this.participants.contains(user))
			return true;
		return false;
	}
	public boolean isPart(List<User> users) {
		if(this.participants.containsAll(users))
			return true;
		return false;
	}
}