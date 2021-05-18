public class Node {
    protected Node parent;
    protected Action action;
    protected Point point;

    public Node(Node parent, Action action, Point point) {
        this.parent = parent;
        this.action = action;
        this.point = point;
    }
}
