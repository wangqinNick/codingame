import javax.management.MBeanRegistration;
import java.util.*;
import java.io.*;
import java.math.*;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
class Solution {

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int N = in.nextInt();
        int M = in.nextInt();
        int L = in.nextInt();

        /* read spots */
        ArrayList<Point> spots = new ArrayList<>();
        for (int i = 0; i < N; i++) {
            int XS = in.nextInt();
            int YS = in.nextInt();
            spots.add(new Point(XS, YS));
        }

        /* read orcs */
        ArrayList<Point> orcs = new ArrayList<>();
        for (int i = 0; i < M; i++) {
            int XO = in.nextInt();
            int YO = in.nextInt();
            orcs.add(new Point(XO, YO));
        }

        /* read links */
        Graph graph = new Graph(N, spots, orcs);
        for (int i = 0; i < L; i++) {
            int N1 = in.nextInt();
            int N2 = in.nextInt();
            graph.addEdge(N1, N2);
        }
        //graph.printGraph();
        int S = in.nextInt();
        int E = in.nextInt();

        BFS bfs = new BFS(N, graph);
        ArrayList<Node> path = bfs.search(S, E);
        if (path == null) {
            System.out.println("IMPOSSIBLE");
        } else {
            Collections.reverse(path);
            ArrayList<Integer> pathIndex = new ArrayList<>();
            pathIndex.add(S);
            for (Node n: path
            ) {
                pathIndex.add(n.index);
            }
            pathIndex.add(E);
            System.out.println(pathIndex.toString().replaceAll("\\[", "").replaceAll("\\]", "").replaceAll(", ", " "));
        }
    }
}

class BFS {
    protected int n;
    protected Graph g;

    public BFS(int n, Graph g) {
        this.n = n;
        this.g = g;
    }

    public ArrayList<Node> search(int startIndex, int endIndex) {
        LinkedList<Node> queue = new LinkedList<>();
        ArrayList<Integer> visited = new ArrayList<>();

        Point startPoint = g.spots.get(startIndex);
        Point endPoint = g.spots.get(endIndex);

        Node startNode = new Node(null, startPoint.x, startPoint.y, startIndex);

        queue.addLast(startNode);
        visited.add(startIndex);

        Node currentNode = null;
        boolean found = false;

        while (!queue.isEmpty()) {
            currentNode = queue.pollFirst();
            if (currentNode.x == endPoint.x && currentNode.y == endPoint.y) {
                found = true;
                break;
            }

            ArrayList<Node> children = g.getChildren(currentNode);
            for (Node child: children) {
                boolean safe = true;
                int index = child.index;
                if (visited.contains(index)) continue;
                double stepDistance = currentNode.distance(child);
                for (Point orc: g.orcs) {
                    if (orc.distance(child) <= stepDistance) safe = false; break;
                }
                if (safe) {
                    queue.addLast(child);
                    visited.add(index);
                }
            }
        }

        if (!found) return null;
        ArrayList<Node> path = new ArrayList<>();
        while (currentNode.parent != null)
        {
            currentNode = currentNode.parent;
            if (currentNode.parent != null)
                path.add(currentNode);
        }
        return path;
    }
}

class Graph {
    protected LinkedList<Integer>[] list;
    protected ArrayList<Point> spots;
    protected ArrayList<Point> orcs;
    protected int n;  // number of spots
    public Graph(int n, ArrayList<Point> spots, ArrayList<Point> orcs) {
        this.n = n;
        this.spots = spots;
        this.orcs = orcs;

        list = new LinkedList[n];
        for (int i = 0; i < n ; i++) {
            list[i] = new LinkedList<>();
        }
    }

    public void printGraph(){
        for (int i = 0; i < n ; i++) {
            if(list[i].size()>0) {
                System.err.print("Point " + i + " is connected to: ");
                System.err.println(list[i]);
            }
        }
    }

    public void addEdge(int source, int destination){

        //add edge
        list[source].addFirst(destination);

        //add back edge ((for undirected)
        list[destination].addFirst(source);
    }

    public ArrayList<Node> getChildren(Node node) {
        LinkedList<Integer> neighboursIndex = list[node.index];
        ArrayList<Node> children = new ArrayList<>();
        for (int index: neighboursIndex) {
            Point child = spots.get(index);
            children.add(new Node(node, child.x, child.y, index));
        }
        return children;
    }
}

class Node {
    protected Node parent;
    protected int x;
    protected int y;
    protected int index;

    public Node(Node parent, int x, int y, int index) {
        this.parent = parent;
        this.x = x;
        this.y = y;
        this.index = index;
    }

    public double distance(Point other) {
        return  Math.sqrt((x - other.x)*(x - other.x) + (y - other.y)*(y - other.y));
    }

    public double distance(Node other) {
        return  Math.sqrt((x - other.x)*(x - other.x) + (y - other.y)*(y - other.y));
    }
}

class Point {
    protected int x;
    protected int y;
    protected int index;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public double distance(Point other) {
        return  Math.sqrt((x - other.x)*(x - other.x) + (y - other.y)*(y - other.y));
    }

    public double distance(Node other) {
        return  Math.sqrt((x - other.x)*(x - other.x) + (y - other.y)*(y - other.y));
    }
}