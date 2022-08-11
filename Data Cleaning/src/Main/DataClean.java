package Main;

import java.io.*;

public class DataClean {

    public static void main(String[] args) {
        BufferedReader reader;
        String outputPath = "OutputGames.pgn";

        try {
            reader = new BufferedReader(new FileReader(
                    "Data/ficsgamesdb_202201_standard2000_nomovetimes_259055.pgn"));
            String line = reader.readLine();
            while (line != null) {
                writeFile(outputPath, line);
                // read next line
                line = reader.readLine();
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }//Data/ficsgamesdb_202201_standard2000_nomovetimes_259055.pgn

    /**
     * Writes a line to a file if it is a line representing moves in a chess game. Do nohting otherwise
     * @param line The line we will write to a file
     * @param path  The path to the file we will write to
     */
    private static void writeFile(String path, String line) throws IOException {
        if(line.length() == 0 || line.charAt(0) != '1') {
            return;
        }

        String addedLine = line.substring(0, line.lastIndexOf('{'));


        Writer fileWriter = new FileWriter(path, true);
        fileWriter.write(addedLine + "\n");

        fileWriter.close();
    }
}
