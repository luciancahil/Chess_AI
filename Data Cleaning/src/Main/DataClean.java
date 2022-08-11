package Main;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class DataClean {

    public static void main(String[] args) {
        BufferedReader reader;
        try {
            reader = new BufferedReader(new FileReader(
                    "Data/ficsgamesdb_202201_standard2000_nomovetimes_259055.pgn"));
            String line = reader.readLine();
            while (line != null) {
                System.out.println(line);
                // read next line
                line = reader.readLine();
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }//Data/ficsgamesdb_202201_standard2000_nomovetimes_259055.pgn
}
