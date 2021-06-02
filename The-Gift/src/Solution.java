import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Scanner;

public class Solution {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int N = in.nextInt();
        int C = in.nextInt();

        ArrayList<Integer> budgets = new ArrayList<>();
        ArrayList<Integer> payment = new ArrayList<>();

        for (int i = 0; i < N; i++) {
            int B = in.nextInt();
            budgets.add(B);
            payment.add(0);
        }

        int sum = 0;
        for (int i: budgets) {
            sum += i;
        }
        if (sum < C) {
            System.out.println("IMPOSSIBLE");
            return;
        }

        int i = 0;
        while(C > 0){
            int temp_pay = payment.get(i);
            if (temp_pay < budgets.get(i)) {  // still with in ith budget
                C--;
                temp_pay++;
                payment.set(i, temp_pay);
            }
            i++;
            if (i >= budgets.size()) {
                i = 0;
            }
        }

        Collections.sort(payment);
        for (int j: payment
             ) {
            System.out.println(j);
        }
    }
}
