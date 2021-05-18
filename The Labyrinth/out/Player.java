import java.util.ArrayList;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;
import java.util.Scanner;

class Player {
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
class Action {
    protected String act;

    public Action(String act) {
        this.act = act;
    }
}


class BFS {
    protected final int[] DR = new int[]{-1, 1, 0, 0};  // up, down, right, left
    protected final int[] DC = new int[]{0, 0, 1, -1};
    //protected int n;
    protected Maze maze;

    public BFS(Maze maze) {
        this.maze = maze;
    }

    public ArrayList<Node> getChildren(Node currentNode) {
        ArrayList<Node> children = new ArrayList<>();
        int r = currentNode.point.y;
        int c = currentNode.point.x;
        if (maze.data[r][c] == '#') {
            return null;
        }
        for (int i = 0; i < 4; i++) {
            int rr = r + DR[i];
            int cc = c + DC[i];

            /* skip out of bounds locations */
            if (rr < 0 || cc < 0) continue;
            if (rr >= maze.height || cc >= maze.width) continue;

            /* skip visited locations or blocked cells */
            if (maze.data[rr][cc] == '#') continue;
            //if (maze.data[rr][cc] == '?') continue;
            int nextIndex = maze.cordToIndex(cc, rr);
            Action action;
            switch (i) {
                case 0:
                    action = new Action("UP");
                    break;
                case 1:
                    action = new Action("DOWN");
                    break;
                case 2:
                    action = new Action("RIGHT");
                    break;
                case 3:
                    action = new Action("LEFT");
                    break;
                default:
                    action = null;
            }
            children.add(new Node(currentNode, action, new Point(cc, rr, nextIndex)));
        }
        return children;
    }

    public ArrayList<Action> explore(Point startPoint, char c) {
        boolean found = false;
        LinkedList<Node> queue = new LinkedList<>();
        ArrayList<Integer> visited = new ArrayList<>();
        Node startNode = new Node(null, null, startPoint);
        queue.addLast(startNode);
        Node currentNode = null;

        while (!queue.isEmpty()) {
            currentNode = queue.poll();
            System.err.print("Exploring " + currentNode.point + " ---");
            if (maze.data[currentNode.point.y][currentNode.point.x] == c) {
                found = true;
                System.err.println("found unknown " + currentNode.point);
                break;
            }
            if (visited.contains(currentNode.point.index)) {
                continue;
            }
            visited.add(currentNode.point.index);
            //System.err.println("Exploring2 " + currentNode.point);
            ArrayList<Node> children = getChildren(currentNode);
            if (children == null) continue;
            for (Node childNode: children) {
                int childIndex = childNode.point.index;
                if (visited.contains(childIndex)) continue;
                queue.addLast(childNode);
            }
            System.err.println();
        }

        if (!found) return null;
        ArrayList<Action> path = new ArrayList<>();
        path.add(currentNode.action);
        while (currentNode.parent != null)
        {
            currentNode = currentNode.parent;
            if (currentNode.parent != null) {

                path.add(currentNode.action);
            }
        }
        Collections.reverse(path);
        return path;
    }

    public ArrayList<Node> getChildrenSafe(Node currentNode) {
        ArrayList<Node> children = new ArrayList<>();
        int r = currentNode.point.y;
        int c = currentNode.point.x;
        if (maze.data[r][c] == '#') {
            return null;
        }
        for (int i = 0; i < 4; i++) {
            int rr = r + DR[i];
            int cc = c + DC[i];

            /* skip out of bounds locations */
            if (rr < 0 || cc < 0) continue;
            if (rr >= maze.height || cc >= maze.width) continue;

            /* skip visited locations or blocked cells */
            if (maze.data[rr][cc] == '#') continue;
            if (maze.data[rr][cc] == '?') continue;
            int nextIndex = maze.cordToIndex(cc, rr);
            Action action;
            switch (i) {
                case 0:
                    action = new Action("UP");
                    break;
                case 1:
                    action = new Action("DOWN");
                    break;
                case 2:
                    action = new Action("RIGHT");
                    break;
                case 3:
                    action = new Action("LEFT");
                    break;
                default:
                    action = null;
            }
            children.add(new Node(currentNode, action, new Point(cc, rr, nextIndex)));
        }
        return children;
    }

    public ArrayList<Action> exploreSafe(Point startPoint, char c) {
        boolean found = false;
        LinkedList<Node> queue = new LinkedList<>();
        ArrayList<Integer> visited = new ArrayList<>();
        Node startNode = new Node(null, null, startPoint);
        queue.addLast(startNode);
        Node currentNode = null;

        while (!queue.isEmpty()) {
            currentNode = queue.poll();
            System.err.print("Exploring " + currentNode.point + " ---");
            if (maze.data[currentNode.point.y][currentNode.point.x] == c) {
                found = true;
                System.err.println("found unknown " + currentNode.point);
                break;
            }
            if (visited.contains(currentNode.point.index)) {
                continue;
            }
            visited.add(currentNode.point.index);
            //System.err.println("Exploring2 " + currentNode.point);
            ArrayList<Node> children = getChildrenSafe(currentNode);
            if (children == null) continue;
            for (Node childNode: children) {
                int childIndex = childNode.point.index;
                if (visited.contains(childIndex)) continue;
                queue.addLast(childNode);
            }
            System.err.println();
        }

        if (!found) return null;
        ArrayList<Action> path = new ArrayList<>();
        path.add(currentNode.action);
        while (currentNode.parent != null)
        {
            currentNode = currentNode.parent;
            if (currentNode.parent != null) {

                path.add(currentNode.action);
            }
        }
        Collections.reverse(path);
        return path;
    }

}
class Point {
    protected int x;
    protected int y;
    protected int index;

    public Point(int x, int y, int index) {
        this.x = x;
        this.y = y;
        this.index = index;
    }

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
        this.index = -1;
    }

    @Override
    public String toString() {
        return "Point{" +
                "x=" + x +
                ", y=" + y +
                '}';
    }
}
class Node {
    protected Node parent;
    protected Action action;
    protected Point point;

    public Node(Node parent, Action action, Point point) {
        this.parent = parent;
        this.action = action;
        this.point = point;
    }
}
class ConstantField {
    protected final static char UNKNOWN = '?';
    protected final static char WALL = '#';
    protected final static char EMPTY = '.';
    protected final static char ORIGIN = 'T';
    protected final static char CONTROL_ROOM = 'C';
}

class Maze {
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
