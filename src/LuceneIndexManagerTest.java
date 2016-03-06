import java.io.IOException;

import org.apache.lucene.document.Document;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.search.TermQuery;

public class LuceneIndexManagerTest {

	static final String INDEX_PATH = "indexDir";
	static final String JSON_FILE_PATH = "out/termlist.json";
	static final String QUERY_FILE_PATH = "termlist.json";
	static final String QUERY_KEYWORD = "Bid Size";
	static final int HITS_PER_PAGE = 10;
	
	public static void main(String[] args) throws ParseException, IOException {
		// TODO Auto-generated method stub
//		 System.out.println("Working Directory = " +
//	             System.getProperty("user.dir"));
		
		IndexManager im = new IndexManager(INDEX_PATH, JSON_FILE_PATH);
		
		im.init();
		int rows = im.createIndex();
		
//		System.out.println("Number of rows :" + rows);
			
			
		im.createQuery(QUERY_FILE_PATH, QUERY_KEYWORD);
		im.search(HITS_PER_PAGE);
        im.display();
		im.finish();
	}

}
