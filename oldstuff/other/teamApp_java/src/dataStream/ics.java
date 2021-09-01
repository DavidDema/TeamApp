package dataStream;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import competition.Competition;
import competition.Team;
import competition.event.Event;
import competition.event.Game;
import main.teamApp;

public class ics {

	/*
BEGIN:VEVENT
DTSTAMP:20210527T094910Z
DTSTART:20200919T140000Z
DURATION:PT1H40M
SUMMARY:DSG Großglockner Falken : DSG Südtirol 16
DESCRIPTION:DSG 1. Klasse D (2. Runde)
UID:2805686
X-HOMENR:1828
X-AWAYNR:1800
URL:https://www.oefb.at/bewerbe/Spiel/2805686/?DSG-Grossglockner-Falken-vs-
 DSG-Suedtirol-16
LOCATION:Nachwuchszentrum Vienna / Gem. Wien 20 (Spielmanng. 8\, 1200 Wien)
 
END:VEVENT
	 */
	List<String> t = Arrays.asList("BEGIN:", "DTSTAMP:", "DTSTART:", "DURATION:", "SUMMARY:", "DESCRIPTION:",
									"UID:", "X-HOMENR:", "X-AWAYNR", "URL:", "LOCATION:", "END:");
	
	public ics(String filename) {
		
		List<String> gt = new ArrayList<String>();
		List<String> input = InputData.processInputFile(filename,0);
		
		for(int i=0;i<input.size();i++) {
			String element = input.get(i);
			
			if(element.contains(t.get(0))) {
				//System.out.println("Begin");
			}
				
			if(element.contains(t.get(t.size()-1))) {
				//System.out.println("End");
				//System.out.println(gt);
				if(gt.size()>0)
					teamApp.addGamesICS(gt);
				gt.clear();
			}
			
			for(int j=0; j<t.size();j++) {
				ics.getVal(element, t.get(j), gt);
			}
		}
	}
	
	public static boolean getVal(String input, String t, List<String> list) {
		if(input.contains(t)) {
			list.add(input.substring(t.length()));
			return true;
		}
		return false;
	}
	
	public static List<String> getTeamText(String text){
		List<String> list = new ArrayList<String>();
		//System.out.print(text+ "\n");
		int index = text.indexOf(":");
		//System.out.print("index"+index+ "\n");
		list.add(text.substring(0, index-1));
		list.add(text.substring(index+2, text.length()));
		//System.out.print(list+"\n");
		
		return list;
	}
	
	public static List<String> getCompetitionText(String text){
		List<String> list = new ArrayList<String>();
		//System.out.print(text+ "\n");
		
		int index = text.indexOf("(");
		//System.out.print("index"+index+ "\n");
		
		list.add(text.substring(0, index-1));
		list.add(text.substring(index+1, index+2));
		//System.out.print(list+"\n");
		
		return list;
	}
}
