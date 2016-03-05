import java.io.IOException;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.RAMDirectory;

public class IndexManager {
	
	String indexPath;
	String jsonFilePath;
	IndexWriter indexWriter = null;
	
    IndexManager(String indexPath, String jsonFilePath){
    	this.indexPath = indexPath;
    	this.jsonFilePath = jsonFilePath;
    		 
    }
    
    public boolean createIndex(){
    	try{
	    	
    		if(indexWriter == null) 
    			return false;
    		
//    		create(); // get json data into document
	        
	       	Document doc = new Document();
	       	// add fileds
	        indexWriter.addDocument(doc);
	        
	    } catch (IOException ex) {
	    	System.err.println("Error creating index. " +  ex.getMessage());
	    } 
    	
        return true;
    }
    
    public boolean createQuery(){
    	try{
    
    	}catch (IOException ex) {
	    	System.err.println("Error creating query. " +  ex.getMessage());
	    }
		return true; 
    }
    
    private boolean init(){
        try {
            StandardAnalyzer analyzer = new StandardAnalyzer();

            Directory index = new RAMDirectory();
            IndexWriterConfig config = new IndexWriterConfig(analyzer);
            indexWriter = new IndexWriter(index, config);

            return true;
        } catch (Exception e) {
            System.err.println("Error opening the index. " + e.getMessage());
        }
        return false;
    }
    
    private void finish(){
        try {
            indexWriter.commit();
            indexWriter.close();
//            reader.close();
        } catch (IOException ex) {
            System.err.println("We had a problem closing the index: " + ex.getMessage());
        }
    }    
      
}