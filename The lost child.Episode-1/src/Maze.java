import java.util.Scanner;

public class Maze {
    protected final static int height = 10;
    protected final static int width = 10;
    protected char[][] data;

    public Maze(Scanner in) {
        this.data = new char[height][width];
        for (int i = 0; i < 10; i++) {  // y
            String row = in.nextLine();
            for (int j = 0; j < row.length(); j++) {  // x
                char c = row.charAt(j);
                data[i][j] = c;
            }
        }
    }

    public static int cordToIndex(int x, int y) {
        /*
        x: -- >
         */
        return y * width + x;
    }
}
