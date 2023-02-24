package inverted.java;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;


public class inverted_index {

    public static void main(String[] args) throws IOException{ 
    	
            BufferedReader reader = new BufferedReader(new FileReader("C:\\Users\\admin\\Downloads\\testfile\\input.big"));
 
            Path path = Paths.get("C:\\Users\\admin\\Downloads\\testfile\\input.big");
            int lineCount = (int) Files.lines(path).count();
            int Count = 0;
            String[] sentence = new String[lineCount];        
            String sent;
            while (reader.readLine() != null) {
            	sent = reader.readLine();
            	sentence[Count]= sent;
                Count++;
                
                
            }
            HashMap<String, HashMap<Integer,Integer>> doc = new HashMap<String, HashMap<Integer,Integer>>();
            
            for (int i = 0; i < sentence.length; i++) {
            	if (sentence[i] !=null) {
	            String[] temp = sentence[i].toLowerCase().replaceAll("[^a-z0-9]", " ").split(" ");
	            for (int j =0 ; j<temp.length; j++) {
	            	String word = temp[j];
	            	HashMap<Integer, Integer> docInfo = new HashMap<>();
	            	int docid = Integer.parseInt(temp[0]);
	            	if (doc.containsKey(word)) {
	            		docInfo = doc.get(word);
	            		if (docInfo.containsKey(i)) {
	            			int count = docInfo.get(i);
	            			docInfo.put(docid, count + 1);
	            		} else {
	            			docInfo.put(docid, 1);
	            		}
	            	} else {
	            		docInfo.put(docid, 1);
	            		doc.put(word, docInfo);
	            	}
	            	
	            	
	            }
	        }}
            for (Entry<String, HashMap<Integer, Integer>> entry : doc.entrySet()) {
            	String word = entry.getKey();
            	HashMap<Integer, Integer> docInfo = entry.getValue();

            	System.out.println(word + ":");
            	for (Entry<Integer, Integer> entry2 : docInfo.entrySet()) {
            	int docid = entry2.getKey();
            	int count = entry2.getValue();    
            	System.out.println("   " + docid + ": " + count);
            
            }}
    }}
           
    		
