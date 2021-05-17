public class Node {
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
