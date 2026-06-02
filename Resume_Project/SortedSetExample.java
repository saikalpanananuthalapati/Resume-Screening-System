import java.util.SortedSet;
import java.util.TreeSet;
public class SortedSetExample {
 public static void main(String[] args) {
 System.out.println("\nSortedSet Example:");
 SortedSet<Integer> set = new TreeSet<>();
 set.add(50);
 set.add(10);
 set.add(40);
 set.add(20);
 set.add(30);
 System.out.println("Initial SortedSet: " + set);
 set.remove(30);
 System.out.println("After removing 30: " + set);
 System.out.println("First Element: " + set.first());
 System.out.println("Last Element: " + set.last());
 System.out.println("Contains 20? " + set.contains(20));
 System.out.println("Size: " + set.size());
 System.out.println("Iterating through SortedSet:");
 for (Integer num : set) {
 System.out.println(num);
 }
 set.clear();
 System.out.println("SortedSet after clearing: " + set);
 }
}  