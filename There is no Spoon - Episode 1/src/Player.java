import java.util.Scanner;

class Player {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int width = in.nextInt(); // the number of cells on the X axis
        int height = in.nextInt(); // the number of cells on the Y axis

        char[][] grid = new char[height][width];

        if (in.hasNextLine()) {
            in.nextLine();
        }

        for (int i = 0; i < height; i++) {
            String line = in.nextLine(); // width characters, each either 0 or .
            for (int j = 0; j < line.length(); j++) {
                char c = line.charAt(j);
                grid[i][j] = c;
            }
        }

        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                System.err.print(grid[i][j]);
            }
            System.err.println();
        }

        int[] dirX = {1, 0};  // right, down
        int[] dirY = {0, 1};  // right, down

        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                // this point
                int nextX = j;
                int nextY = i;
                if (grid[nextY][nextX] == '.') {
                    continue;
                }
                System.out.print(nextX + " " + nextY);

                // check right
                nextX = j + 1;
                nextY = i;
                boolean found = false;
                while(nextX < width) {

                    if (grid[nextY][nextX] != '.') {
                        System.out.print(" " + nextX + " " + nextY);
                        found = true;
                        break;
                    }
                    nextX += 1;
                }

                if (!found) {
                    System.out.print(" " + -1 + " " + -1);
                }

                // check right
                nextX = j;
                nextY = i + 1;
                found = false;

                while(nextY < height) {
                    if (grid[nextY][nextX] != '.') {
                        System.out.print(" " + nextX + " " + nextY);
                        found = true;
                        break;
                    }

                    nextY += 1;
                }

                if (!found) {
                    System.out.print(" " + -1 + " " + -1);
                }

                System.out.println();
            }
        }
    }
}
