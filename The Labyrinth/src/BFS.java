
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;

public class BFS {
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
