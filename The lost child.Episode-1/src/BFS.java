import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;

public class BFS {
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
