import java.util.ArrayList;
import java.util.Scanner;

public class Solution {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        Maze maze = new Maze(in);
        int currentIndex, nextIndex;
        Graph g = new Graph(Maze.height, Maze.width);
        final int[] DR = new int[]{-1, 1, 0, 0};  // up, down, left, right
        final int[] DC = new int[]{0, 0, 1, -1};

        Point startPoint = null, endPoint = null;

        for (int r = 0; r < Maze.height; r++) {
            for (int c = 0; c < Maze.width; c++) {
                if (maze.data[r][c] == '#') continue;  //ignore walls
                if (maze.data[r][c] == 'M') startPoint = new Point(c, r);
                if (maze.data[r][c] == 'C') endPoint = new Point(c, r);
                currentIndex = Maze.cordToIndex(c, r);
                for (int i = 0; i < 4; i++) {
                    int rr = r + DR[i];
                    int cc = c + DC[i];

                    /* skip out of bounds locations */
                    if (rr < 0 || cc < 0) continue;
                    if (rr >= Maze.height || cc >= Maze.width) continue;

                    /* skip visited locations or blocked cells */
                    if (maze.data[rr][cc] == '#') continue;

                    /* connect edges */
                    nextIndex = Maze.cordToIndex(cc, rr);
                    g.addEdge(currentIndex, nextIndex);
                }
            }
        }

//        g.printGraph();



        BFS bfs = new BFS(g.width * g.height, g);
        ArrayList<Point> path = bfs.solve(startPoint, endPoint);
        for (Point point: path) {
            System.err.print(point + " ");
        }

        System.out.println((path.size()+1)*10 + "km");
    }
}
