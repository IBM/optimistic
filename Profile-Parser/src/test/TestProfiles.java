package test;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;

import com.ibm.hrl.eco.abstractions.ProfilesLexer;
import com.ibm.hrl.eco.abstractions.ProfilesParser;
import com.ibm.hrl.eco.abstractions.ProfilesParser.ProfileContext;

public class TestProfiles {
	public static void main(String[] args) throws IOException {
		BufferedReader inp = new BufferedReader(new FileReader(args[0]));
		String profile;
		profile = inp.readLine().trim();
		int errs = 0;
		while (profile != null) {
			if (profile.length() != 0) {
//				System.out.println(profile);
				CharStream cs = CharStreams.fromString(profile);
				ProfilesLexer lexer = new ProfilesLexer(cs);
				CommonTokenStream tokens = new CommonTokenStream(lexer);
				ProfilesParser parser = new ProfilesParser(tokens);
				ProfileContext tree = parser.profile();
//				System.out.println(tree.toStringTree(parser));
				String flat = tree.toStringTree(parser).trim();
				String ref = inp.readLine().trim();
				if (!flat.equals(ref)) {
					errs++;
					System.out.println("*** Mismatch for profile: " + profile);
					System.out.println("Expected: " + ref);
					System.out.println("Actual:   " + flat);
				}
			}
			profile = inp.readLine();
		}
		System.out.println("Total errors: " + errs);
		inp.close();
	}

}
