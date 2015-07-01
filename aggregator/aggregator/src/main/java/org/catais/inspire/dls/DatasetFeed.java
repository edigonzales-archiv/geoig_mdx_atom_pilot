package org.catais.inspire.dls;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.rometools.rome.feed.synd.SyndEntry;
import com.rometools.rome.feed.synd.SyndFeed;
import com.rometools.rome.feed.synd.SyndLink;
import com.rometools.rome.io.FeedException;
import com.rometools.rome.io.SyndFeedInput;
import com.rometools.rome.io.XmlReader;

public class DatasetFeed {
		static final Logger logger = LogManager.getLogger(DatasetFeed.class.getName());
		
		private String datasetFeedUrl;
		private String feedTitle;
		private Date updated;
		private String datasetFeedLink;
		private String datasetFeedDescriptionLink;
		private String serviceFeedLink;
		private ArrayList<DatasetFeedEntry> datasetAlternatives = new ArrayList<DatasetFeedEntry>();
		
		public DatasetFeed(String datasetFeedUrl) throws MalformedURLException, IOException, FeedException {
	        this.datasetFeedUrl = datasetFeedUrl;   
	        init();
		}
		
		private void init() throws MalformedURLException, IOException, FeedException {
			URL url  = new URL(datasetFeedUrl);
	    	XmlReader reader = null;

	    	reader = new XmlReader(url);
	    	SyndFeed feed = new SyndFeedInput().build(reader);
	    	
	    	feedTitle = feed.getTitle();
	    	updated = feed.getPublishedDate();
	    	
	    	// get opensearch and metadata link
	        List<SyndLink> links = feed.getLinks();
	        for (SyndLink link: links) {
	        	String rel = link.getRel();
	        	
	        	if (rel.equalsIgnoreCase("self")) {
	        		datasetFeedLink = link.getHref();
	        	} else if (rel.equalsIgnoreCase("describeby")) {
	        		datasetFeedDescriptionLink = link.getHref();
	        	} else if (rel.equalsIgnoreCase("up")) {
	        		serviceFeedLink = link.getHref();
	        	}
	        }  
	    	
	        logger.debug(feedTitle);
	        
	    	// get all dataset feed entries
	    	List<SyndEntry> entries = feed.getEntries();
	    	for (SyndEntry entry: entries) {    
	    		DatasetFeedEntry dfe = new DatasetFeedEntry(entry);
	    		datasetAlternatives.add(dfe);
	    	}
		}

		public ArrayList getDatasetAlternatives() {
			return datasetAlternatives;
		}
}
