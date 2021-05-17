import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Scanner;

class BFS {
    protected int n;
    protected Graph g;

    public BFS(int n, Graph g) {
        this.n = n;
        this.g = g;
    }

    public ArrayList<Point> solve(Point start, Point goal) {
        boolean found = false;

        LinkedList<Node> queue = new LinkedList<>();

        ArrayList<Integer> visited = new ArrayList<>();

        Node startNode = new Node(null, start.x, start.y, 0, Maze.cordToIndex(start.x, start.y));

        queue.addLast(startNode);
        visited.add(startNode.index);

        Node currentNode = null;
        while (!queue.isEmpty()) {
            currentNode = queue.poll();
            if (currentNode.x == goal.x && currentNode.y == goal.y) {
                found = true;
                break;
            }
            for (Node childNode: g.getChildren(currentNode)) {
                int childIndex = childNode.index;
                if (visited.contains(childIndex)) continue;
                queue.addLast(childNode);
                visited.add(childIndex);
            }
        }
        if (!found) return null;
        ArrayList<Point> path = new ArrayList<>();
        while (currentNode.parent != null)
        {
            currentNode = currentNode.parent;
            if (currentNode.parent != null)
                path.add(new Point(currentNode.x, currentNode.y));
        }
        return path;
    }
}
class Point {
    protected int x;
    protected int y;
    protected int index;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
        this.index = Maze.cordToIndex(x, y);
    }

    @Override
    public String toString() {
        return "Point{" +
                "x=" + x +
                ", y=" + y +
                '}';
    }
}

class Graph {
    protected int height;
    protected int width;
    protected int n;
    LinkedList<Integer>[] list;

    public Graph(int height, int width) {
        this.height = height;
        this.width = width;
        n = height * width;
        list = new LinkedList[n];
        for (int i = 0; i < n ; i++) {
            list[i] = new LinkedList<>();
        }
    }

    public void addEdge(int source, int destination){

        //add edge
        list[source].addFirst(destination);

        //add back edge ((for undirected)
        // list[destination].addFirst(source);
    }

    public void printGraph(){
        for (int i = 0; i < n ; i++) {
            if(list[i].size()>0) {
                System.err.print("Point " + i + " is connected to: ");
                System.err.println(list[i]);
            }
        }
    }

    public ArrayList<Node> getChildren(Node node) {
        ArrayList<Node> children = new ArrayList<>();
        LinkedList<Integer> neighboursIndex = list[node.index];
        int x, y;
        for (int i: neighboursIndex) {  // i = 13
            x = i % width;  // x = 2, height = 11
            y = Math.floorDiv(i, width);  // y = 1
            // Log.log("index: " + i + "-> point: (" + x + ", " + y + ")");
            children.add(new Node(node, x, y, 0, i));
        }
        return children;
    }
}
class Node {
    protected Node parent;
    protected int x;
    protected int y;
    protected int distance;
    protected int index;

    public Node(Node parent, int x, int y, int distance, int index) {
        this.parent = parent;
        this.x = x;
        this.y = y;
        this.distance = distance;
        this.index = index;
    }
}

class Solution {
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

class Maze {
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
