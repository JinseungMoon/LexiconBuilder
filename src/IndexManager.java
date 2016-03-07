import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TermQuery;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;

import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class IndexManager {
	
	// POJOs
    public static class TermData{
    	private String term;
    	private String url;
    	private String definition;
    	private String breakdown;
    	
    	public static class TermPair{
    		private String term;
    		private String url;
    		
    		public String getTerm() { return this.term; }
    		public String getUrl() { return this.url; }
    		
    		public void setTerm(String term) { this.term = term; }
    		public void setUrl(String url) { this.url = url; }
    	}
    	private List<TermPair> relatedTerms;
    	private List<TermPair> anchorTerms;
    	
    	
    	public String getTerm() { return this.term; }
    	public String getUrl() { return this.url; }
    	public String getDefinition() { return this.definition; }
    	public String getBreakdown() { return this.breakdown; }
    	public List<TermPair> getRelatedTerms() { return this.relatedTerms; }
    	public List<TermPair> getAnchorTerms() { return this.anchorTerms; }
    	
    	public void setTerm(String term) { this.term = term; }
    	public void setUrl(String url) { this.url = url; }
    	public void setDefinition(String definition) { this.definition = definition; }
    	public void setBreakdown(String breakdown) { this.breakdown = breakdown; }
    	public void setRelatedTerms(List<TermPair> relatedTerms) { this.relatedTerms = relatedTerms;}
    	public void setAnchorTerms(List<TermPair> anchorTerms) { this.anchorTerms = anchorTerms;}
    	
    	public void appendAnchorPair(TermPair anchorPair) { this.anchorTerms.add(anchorPair); } 
    }
    
    public static class UrlData{
    	private String term;
    	private String url;
    	
    	public String getTerm() { return this.term; }
    	public String getUrl() { return this.url; }
   
    	
    	public void setTerm(String term) { this.term = term; }
    	public void setUrl(String url) { this.url = url; }
    }
  
  
    List<TermData> termDataList;
    List<UrlData> urlDataList;
    
    private String indexPath;
    private String termFilePath; 
    private String urlFilePath;
    
    ObjectMapper mapper; 
    
    
	private Directory index = null;
	private IndexWriterConfig config = null;
	private IndexWriter indexWriter = null;
	private Analyzer analyzer = null;
	private IndexReader reader = null;
	private IndexSearcher searcher = null;
	private ScoreDoc[] hits;
	    
    public boolean init(String indexPath, String termFilePath, String urlFilePath){
    	this.indexPath = indexPath;
    	this.termFilePath = termFilePath;
    	this.urlFilePath = urlFilePath;
    	
        try {
            analyzer = new StandardAnalyzer();
            index = new RAMDirectory();
            config = new IndexWriterConfig(analyzer);
            indexWriter = new IndexWriter(index, config);
            
            
            // stream json files to class objects
            mapper = new ObjectMapper(); // can reuse, share globally
        	termDataList = mapper.readValue(new File(termFilePath), new TypeReference<List<TermData>>(){});
    		urlDataList = mapper.readValue(new File(urlFilePath), new TypeReference<List<UrlData>>(){});
    		
//    		for( int i = 0; i < termDataList.size() ; i++){
//    			if( termDataList.get(i).getRelatedTerms() != null)
//    				System.out.println(termDataList.get(i).getRelatedTerms()[0].getTerm());	 
//    		}
//    		
    		
    		
        } catch (Exception e) {
            System.err.println("Error opening." + e.getMessage());
        }
        return true;
    }
    
    public void finish(){
        try {
        	if(reader != null) {reader.close();}
        } catch (IOException ex) {
            System.err.println("Error closing" + ex.getMessage());
        }
    }
   
    // create index from term.json file
    public int createIndex(String indexPath, String termFilePath) throws JsonParseException, JsonMappingException, IOException{
		// create Lucene document object
		Document doc = new Document();
	
		for(TermData t : termDataList){
//			System.out.println(u.getTerm());
//			doc.add(new StringField("term", t.getTerm(), Field.Store.NO));
//			doc.add(new StringField("url", t.getUrl(), Field.Store.NO));
			doc.add(new TextField(t.getTerm(), t.getDefinition().toLowerCase(), Field.Store.NO));
			doc.add(new TextField(t.getTerm(), t.getBreakdown().toLowerCase(), Field.Store.NO));
//			doc.add(new StringField("url", t.getBreakdown(), Field.Store.NO));
//    			doc.add(new TextField("description", "A beautiful hotel", Field.Store.YES));
		}
		
		indexWriter.addDocument(doc);
		
	    indexWriter.commit();
        indexWriter.close();
	
        return termDataList.size();
    }
    
	public void match() throws JsonGenerationException, JsonMappingException, IOException {
		
		// parse json file
		

	}

    // search each term's data and find all links from the data
	public boolean search(int hitsPerPage) throws IOException, ParseException {   
        
		reader = DirectoryReader.open(index);
        searcher = new IndexSearcher(reader);
        
		int count = 0;
		for(TermData t : termDataList){	
			for( UrlData u  : urlDataList ){
	        	TermQuery queryStr = new TermQuery(new Term(t.getTerm(), u.getTerm().toLowerCase()));

	        	TopDocs docs = searcher.search(queryStr, hitsPerPage);
	            hits = docs.scoreDocs;
	    		
	            if( hits.length > 0){
	            	boolean flag_contained = false;
		            for( TermData.TermPair oldPair : t.getAnchorTerms() ){
		            	if( oldPair.getTerm().toLowerCase().equals(u.getTerm().toLowerCase()) ){
		            		flag_contained = true;
		            	}
		            }
		            
		            if(flag_contained){
		            	continue;
		            }else{
		            	TermData.TermPair newPair = new TermData.TermPair();
		            	newPair.setTerm(u.getTerm());
		            	newPair.setUrl(u.getUrl());
		            	t.appendAnchorPair(newPair);
			            count++;
		            }
	            }
			}
		
		}
		
		mapper.writeValue(new File( this.termFilePath.replace(".json", "-modified.json")), termDataList);
		System.out.println(count + " missing links added.");
     
        return true;
	}    
}