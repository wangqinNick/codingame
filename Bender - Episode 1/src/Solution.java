import java.util.*;
import java.io.*;
import java.math.*;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
class Solution {

    public static void main(String[] args) {

        int[] dirRow = {1, 0, -1, 0};
        int[] dirCol = {0, 1, 0, -1};
        int SOUTH = 0;
        int EAST = 1;
        int NORTH = 2;
        int WEST = 3;

        int[] dir = {SOUTH, EAST, NORTH, WEST};

        Scanner in = new Scanner(System.in);
        int L = in.nextInt();
        int C = in.nextInt();

        char [][] map = new char[L][C];


        if (in.hasNextLine()) {
            in.nextLine();
        }

        /* vars to store Bender's status */
        boolean breakerMode = false;
        boolean inverted = false;
        boolean isDead = false;
        boolean firstMove = true;
        int currentDirection = 0;
        int benderRow = -1, benderCol = -1;

        int[][] transporters = new int[2][2];
        int index = 0;
        for (int i = 0; i < L; i++) {
            String row = in.nextLine();
            for (int j = 0; j < row.length(); j++) {
                char c = row.charAt(j);
                map[i][j] = c;
                if (c == '@') {
                    benderRow = i;
                    benderCol = j;
                }

                if (c == 'T') {
                    transporters[index][0] = i;
                    transporters[index][1] = j;
                    index++;
                }
            }
        }

//        for (int i = 0; i < L; i++) {
//            for (int j = 0; j < C; j++) {
//                System.out.print(map[i][j]);
//            }
//            System.out.println();
//        }
//
//        System.out.println(benderRow + "   " + benderCol);
        ArrayList<String> actions = new ArrayList<>();
        int counter = 0;

        do {
            int tempRow = dirRow[dir[currentDirection]] + benderRow;
            int tempCol = dirCol[dir[currentDirection]] + benderCol;

            int dirIndex = -1;
            //System.out.println(tempRow + "   " + tempCol);

            while ((map[tempRow][tempCol] == '#') || (map[tempRow][tempCol] == 'X' && !breakerMode)) {
                if (inverted) {
                    dirIndex--;
                    if (dirIndex < 0) {
                        dirIndex = 3;
                    }
                } else {
                    dirIndex++;
                    if (dirIndex > 3) {
                        dirIndex = 0;
                    }
                }
                tempRow = dirRow[dir[dirIndex]] + benderRow;
                tempCol = dirCol[dir[dirIndex]] + benderCol;
                currentDirection = dirIndex;
            }

            benderRow += dirRow[dir[currentDirection]];
            benderCol += dirCol[dir[currentDirection]];

            if (map[benderRow][benderCol] == 'X') {
                if (breakerMode) {
                    map[benderRow][benderCol] = ' ';
                }
            }

            switch (currentDirection) {
                case 0:
                    actions.add("SOUTH");
                    break;
                case 1:
                    actions.add("EAST");
                    break;
                case 2:
                    actions.add("NORTH");
                    break;
                case 3:
                    actions.add("WEST");
                    break;
            }

            switch (map[benderRow][benderCol]) {
                case '$':
                    isDead = true;
                    for (String s : actions
                    ) {
                        System.out.println(s);
                    }
                    return;

                // path modifiers
                case 'S':
                    currentDirection = SOUTH;
                    break;
                case 'E':
                    currentDirection = EAST;
                    break;
                case 'N':
                    currentDirection = NORTH;
                    break;
                case 'W':
                    currentDirection = WEST;
                    break;

                // inverter
                case 'I':
                    inverted = !inverted;
                    break;

                // breaker mode
                case 'B':
                    if (!breakerMode) {
                        breakerMode = true;
                    } else {
                        breakerMode = false;
                    }
                    break;

                // transport
                case 'T':
                    if (benderRow == transporters[0][0] && benderCol == transporters[0][1]) {
                        benderRow = transporters[1][0];
                        benderCol = transporters[1][1];
                    } else {
                        benderRow = transporters[0][0];
                        benderCol = transporters[0][1];
                    }
                    break;
            }

            counter++;
            if (counter > 200) {
                System.out.println("LOOP");
                return;
            }
        } while (true);
    }
}