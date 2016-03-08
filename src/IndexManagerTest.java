import java.io.IOException;
import org.apache.lucene.queryparser.classic.ParseException;

public class IndexManagerTest {

	static final String INDEX_PATH = "indexDir";
	static final String TERM_FILE_PATH = "out/term_d.json";
	static final String URL_FILE_PATH = "out/urlList_all.json";
	static final String QUERY_KEYWORD = "A*";
	static final int HITS_PER_PAGE = 10;
	
	public static void main(String[] args) throws ParseException, IOException {
		// TODO Auto-generated method stub
		 System.out.println("Working Directory = " +
	             System.getProperty("user.dir"));
		
		IndexManager im = new IndexManager();
		
		im.init(INDEX_PATH, TERM_FILE_PATH, URL_FILE_PATH);
		int rows = im.createIndex(INDEX_PATH, TERM_FILE_PATH);
		im.match();
		
		im.search(HITS_PER_PAGE);
//      im.display();
		im.finish();
	}

}
