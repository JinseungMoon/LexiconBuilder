import java.io.File;
import java.io.IOException;
import java.util.List;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TermQuery;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class IndexManager {
	
	String indexPath;
	String jsonFilePath;
	String queryFilePath;
	String queryKeyword;
	int hitsPerPage;
	
	Directory index = null;
	IndexWriterConfig config = null;
	IndexWriter indexWriter = null;
	Analyzer analyzer = null;
	IndexReader reader = null;
	IndexSearcher searcher = null;
	TermQuery queryStr;
	ScoreDoc[] hits;
	
	
    IndexManager(String indexPath, String jsonFilePath){
    	this.indexPath = indexPath;
    	this.jsonFilePath = jsonFilePath;
    }
    
    public boolean init(){
        try {
            analyzer = new StandardAnalyzer();
            index = new RAMDirectory();
            config = new IndexWriterConfig(analyzer);
            indexWriter = new IndexWriter(index, config);
            
        } catch (Exception e) {
            System.err.println("Error opening." + e.getMessage());
        }
        return true;
    }
    
    public void finish(){
        try {
            reader.close();
        } catch (IOException ex) {
            System.err.println("Error closing" + ex.getMessage());
        }
    }
    
    static public class UrlList{
    	
    	private String term;
    	private String url;
    	
    	public String getTerm() { return this.term; }
    	public String getUrl() { return this.url; }
    	
    	public void setTerm(String term) { this.term = term; }
    	public void setUrl(String url) { this.url = url; }
    }
    
    public int createIndex() throws JsonParseException, JsonMappingException, IOException{
		if(indexWriter == null) 
			return 0;
		
		// create Lucene document object
		Document doc = new Document();
		
		// parse json file
		ObjectMapper mapper = new ObjectMapper(); // can reuse, share globally
		List<UrlList> urlList = mapper.readValue(new File(jsonFilePath), new TypeReference<List<UrlList>>(){});
		
		for(UrlList u : urlList){
//			System.out.println(u.getTerm());
			doc.add(new StringField("term", u.getTerm(), Field.Store.NO));
			doc.add(new StringField("url", u.getUrl(), Field.Store.NO));
//    			doc.add(new TextField("description", "A beautiful hotel", Field.Store.YES));
		}
		
		indexWriter.addDocument(doc);
		
	    indexWriter.commit();
        indexWriter.close();
	
        return urlList.size();
    }
    
    public boolean createQuery(String queryFilePath, String queryKeyword) throws ParseException{
    	
    	this.queryFilePath = queryFilePath;
    	this.queryKeyword = queryKeyword;

    	queryStr = new TermQuery(new Term("term", queryKeyword));
		return true; 
    }


	public boolean search(int hitsPerPage) throws IOException {
        this.hitsPerPage = hitsPerPage;
        
        reader = DirectoryReader.open(index);
        searcher = new IndexSearcher(reader);
        
        TopDocs docs = searcher.search(queryStr, hitsPerPage);
        hits = docs.scoreDocs;
        System.out.println(hits.length);
		
        return true;
	}    
	
	public void display() throws IOException {
	     // 4. display results
       System.out.println("Found " + hits.length + " hits.");
       for(int i=0;i<hits.length;++i) {
           int docId = hits[i].doc;
           Document d = searcher.doc(docId);
           System.out.println((i + 1) + ". " + d.get("term") + "\t" + d.get("url"));
       }

	}
	

}