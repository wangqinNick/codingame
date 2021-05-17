import java.util.ArrayList;
import java.util.LinkedList;

public class Graph {
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
