package dataStream;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import competition.Team;
import competition.event.Game;
import user.subuser.Player;

public class InputData {
	
	public static List<String> processInputFile(String inputFilePath, int skipLines) {
	    
		List<String> p = new ArrayList<String>();
		
	    try{

	      File inputF = new File(inputFilePath);
	      InputStream inputFS = new FileInputStream(inputF);
	      BufferedReader br = new BufferedReader(new InputStreamReader(inputFS));
	      
	      // skip the header of the csv
	      p = br.lines().skip(skipLines).collect(Collectors.toList());
	      br.close();
	      return p;
	    } catch (IOException e) {
	    }
	    System.out.println("InputFile failed to open");
	    return null;
	}
}
