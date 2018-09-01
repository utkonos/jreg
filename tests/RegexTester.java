import java.util.regex.*;

/*
The main function takes two inputs. The first is the regex you would like to find. The second is the content in which you would like to find the regex.
*/
public class RegexTester {
    public static void main(String[] args) {
        String regex = args[0];
        String content = args[1];

        Pattern pat = Pattern.compile(regex);
        Matcher mat = pat.matcher(content);

        boolean found = false;
        while (mat.find()) {
            System.out.println(mat.group().trim());
            found = true;
        }

        if (!found) {
            System.out.println("No matches found!");
        }
    }
}
