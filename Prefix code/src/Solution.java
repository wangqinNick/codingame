import java.util.HashMap;
import java.util.Scanner;

public class Solution {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);

        HashMap<String, Character> dictionary = new HashMap<>();

        int n = in.nextInt();
        for (int i = 0; i < n; i++) {
            String b = in.next();
            int c = in.nextInt();

            dictionary.put(b, (char)c);
        }

        // System.out.println(dictionary);

        String s = in.next();

        StringBuilder result = new StringBuilder();
        boolean found = false;
        int endIndex;

        for (int startIndex = 0; startIndex < s.length(); startIndex = endIndex ) {
            found = false;
            for (endIndex = startIndex + 1; endIndex < s.length() + 1; endIndex++) {
                String subString = s.substring(startIndex, endIndex);
                if (dictionary.containsKey(subString)) {
                    result.append(dictionary.get(subString));
                    found = true;
                    break;
                }
            }

            if (!found) {
                System.out.println("DECODE FAIL AT INDEX " + startIndex);
                break;
            }
        }
        if (found) {
            System.out.println(result);
        }
    }
}

// abracadabra
// abracadabr