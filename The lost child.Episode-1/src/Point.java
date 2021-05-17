public class Point {
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
