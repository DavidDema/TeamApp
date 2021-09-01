package user;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

import competition.event.Event;
import main.teamApp;


public class User {

	public int id;
	public String name;
	public int age;
	public String privateEmail;
	public LocalDate birthday;
	public String surname;
	public String nickname;
	public String companyMail;
	public UserState state;
	public String mobileNumber;
	public String nation;
	public String hometown;
	public String work;
	public CompanyPosition companyPosition;
	public CompanyPosition interested_companyPosition;
	public float clubYears;
	
	public List<Event> events = new ArrayList<Event>();

	public User(int user_id, String input, boolean print) {
		
		String[] p = input.split(",");// a CSV has comma separated lines
		
		String name = p[0];
		
		this.id = user_id;
		this.name = name;
		this.state = UserState.SUGGESTED;
		
		/*
		 this.surname = surname;
		  this.name = name;
		  this.setBirthday(birthday);
		  this.nickname = nickname;
		  this.nation = nation;
		  
		  //user.setTeam(Team.getTeam(team));
		  
		  this.privateEmail = email;
		  this.mobileNumber = mobileNumber;
		  this.hometown = homeTown;
		  this.work = work;
		  this.setPosition("CM");
		 */
	}
	
	public void setState(String state) {
		this.state = UserState.valueOf(state);
	}
	
	public void setBirthday(String date) {
		//this.birthday = LocalDate.parse(date);
		//this.age = LocalDate.now() - this.birthday;
	}

	public boolean eventResponse(Event event, boolean response) {
		if(this.events.contains(event))
			return event.addResponse(this, response);
		return false;			
	}
	
	public String toString() {
		String summary = "\n";
		summary +=
				"ID:"+this.id + "\n"+
				"User name:" + this.name + "\n" +
				"State:" + this.state + "\n" ;
		
		return summary;
	}
}