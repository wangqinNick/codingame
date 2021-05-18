import java.util.ArrayList;
import java.util.Scanner;

public class Player {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int R = in.nextInt(); // number of rows.
        int C = in.nextInt(); // number of columns.
        int A = in.nextInt(); // number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
        Maze maze;
        boolean foundPathToControlRoom = false;
        boolean hasReachedControlRoom = false;

        // game loop
        while (true) {
            int KR = in.nextInt(); // row where Kirk is located. y
            int KC = in.nextInt(); // column where Kirk is located. x
            if (in.hasNextLine()) {
                in.nextLine();
            }
            maze = new Maze(R, C, in);
            maze.print(KR, KC);
            int startPointIndex = maze.cordToIndex(KC, KR);
            Point startPoint = new Point(KC, KR, startPointIndex);
            if (maze.data[KR][KC] == ConstantField.CONTROL_ROOM) hasReachedControlRoom = true;


            // explore
            BFS bfs = new BFS(maze);
            ArrayList<Action> path;
            if (hasReachedControlRoom) {
                path = bfs.exploreSafe(startPoint, ConstantField.ORIGIN);
            } else {
                path = bfs.exploreSafe(startPoint, ConstantField.CONTROL_ROOM);
                if (path == null) {
                    path = bfs.explore(startPoint, ConstantField.UNKNOWN);
                } else {
                    System.err.println("Found path to Control room");
                }
            }
            System.out.println(path.get(0).act); // Kirk's next move (UP DOWN LEFT or RIGHT)
        }
    }
}
