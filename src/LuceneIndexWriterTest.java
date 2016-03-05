import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;

public class LuceneIndexWriterTest {

	static final String INDEX_PATH = "indexDir";
	static final String JSON_FILE_PATH = "termlist.json";
//	static final String QUERY_FILE_PATH = "termlist.json";
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		IndexManager im = new IndexManager(INDEX_PATH, JSON_FILE_PATH);
		
		im.createIndex();
        
//        // 2. query
//        String querystr = args.length > 0 ? args[0] : "finan";
//		im.createQuery(QUERY_FILE_PATH);
//
//        // the "title" arg specifies the default field to use
//        // when no field is explicitly specified in the query.
//        Query q = new QueryParser("title", analyzer).parse(querystr);
//
//        // 3. search
//		im.search(hitsPerPage)
//        int hitsPerPage = 10;
//        IndexReader reader = DirectoryReader.open(index);
//        IndexSearcher searcher = new IndexSearcher(reader);
//        TopDocs docs = searcher.search(q, hitsPerPage);
//        ScoreDoc[] hits = docs.scoreDocs;
//
//		im.display()
//        // 4. display results
//        System.out.println("Found " + hits.length + " hits.");
//        for(int i=0;i<hits.length;++i) {
//            int docId = hits[i].doc;
//            Document d = searcher.doc(docId);
//            System.out.println((i + 1) + ". " + d.get("isbn") + "\t" + d.get("title"));
//        }
//
//        // reader can only be closed when there
//        // is no need to access the documents any more.
//        reader.close();
//		im.finish();
	}

}
