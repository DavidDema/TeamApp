package main;
import java.io.FileInputStream;
import java.io.InputStream;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import competition.*;
import competition.event.Game;
import dataStream.InputData;
import dataStream.ics;
import user.*;
import user.subuser.Player;
import user.subuser.Position;

public class main {

	public static void main(String[] args) {
		
		Competition dsg1K = new League(1, "DSG 1. Klasse D");
		Competition dsgcup = new League(2, "DSG-CUP");
		teamApp.addCompetition(dsg1K);
		teamApp.addCompetition(dsgcup);
		
		teamApp.addTeamsCSV("teams.csv");
		teamApp.addPlayersCSV("players.csv");
		
		
		new ics("sgscal.ics");
		
		System.out.print(teamApp.players);
		//System.out.print(teamApp.games);
		//System.out.print(teamApp.teams.get(2));
		//System.out.print(teamApp.teams.get(2));
		//teamApp.addEventsCSV("games.csv");
		//testImportICS();
		//test_Player2Teams();
		//test1();
		//test_Teams2Competition(dsg_liga);
		//test_GamesImport();
		//Player.addPlayers("test.csv");
	}
	
	
	/*public static void test1() {
		// TODO Auto-generated method stub
		Player p1 = new Player("dasd");
		p1.name = "David Demattio";
		p1.age = 23;
		p1.position = Position.LM;
		
		
		Player p2 = new Player("dsad");
		p2.name = "Franz Break";
		p2.age = 25;
		p2.position = Position.GK;
		
		Team t1 = new Team("SGS16");
		Team t2 = new Team("SGS07");
		
		p1.setTeam(t1);
		p2.setTeam(t1);
		
		System.out.print(p1.toString());
		System.out.print(t1.toString());
		
		Game g1 = new Game("TestGame",LocalDate.now(),"Kendlerstrasse", 150, t1, t2);
		
		System.out.print(g1.toString());
	}*/
}

/*
LocalDateTime date;
		
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");
String text = "2020-04-20 05:12";

date = LocalDateTime.parse(text,formatter);
System.out.print(date);
*/
