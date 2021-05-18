import java.util.Scanner;

public class Maze {
    protected int height;
    protected int width;
    protected char[][] data;  // T: start, C: control, ?: unknown, #: Wall, .: Empty

    public Maze(int height, int width, Scanner in) {
        this.height = height;
        this.width = width;
        this.data = new char[height][width];
        for (int i = 0; i < height; i++) {  // y
            //if (i == 0) continue;
            String row = in.nextLine();
            for (int j = 0; j < row.length(); j++) {  // x
                char c = row.charAt(j);
                data[i][j] = c;
            }
        }
    }

    public void print(int y, int x) {
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                if (i == y && j == x) {
                    System.err.print('A');
                }else {
                    System.err.print(data[i][j]);
                }
            }
            System.err.println();
        }
    }

    public int cordToIndex(int x, int y) {
        /*
        x: -- >
         */
        return y * width + x;
    }
}
