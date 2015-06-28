package org.catais.inspire.dls;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Date;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.rometools.rome.feed.synd.SyndEntry;
import com.rometools.rome.feed.synd.SyndFeed;
import com.rometools.rome.feed.synd.SyndLink;
import com.rometools.rome.io.FeedException;
import com.rometools.rome.io.SyndFeedInput;
import com.rometools.rome.io.XmlReader;

public class DownloadService {
	static final Logger logger = LogManager.getLogger(DownloadService.class.getName());
	
	private String serviceFeedUrl;
	
	private ArrayList<String> datasetNames = new ArrayList<String>();
	private HashMap<String, ServiceFeedEntry> datasets = new HashMap<String, ServiceFeedEntry>();
	private String feedTitle;
	private Date updated;
	private String selfLink;
	private String describebyLink;
	private String searchLink;

	public DownloadService(String serviceFeedUrl) throws MalformedURLException, IOException, FeedException {
        this.serviceFeedUrl = serviceFeedUrl;   
        init();
	}
	
	private void init() throws MalformedURLException, IOException, FeedException {
		URL url  = new URL(serviceFeedUrl);
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
        		selfLink = link.getHref();
        	} else if (rel.equalsIgnoreCase("describeby")) {
        		describebyLink = link.getHref();
        	} else if (rel.equalsIgnoreCase("search")) {
        		searchLink = link.getHref();
        	}
        }  
    	
    	// get all service feed entries
    	List<SyndEntry> entries = feed.getEntries();
    	for (SyndEntry entry: entries) {    		
    		ServiceFeedEntry sfe = new ServiceFeedEntry(entry);
    		datasets.put(sfe.getSpatialDatasetIdentifierCode(), sfe);   
 
    		datasetNames.add(sfe.getTitle());
    	}
    	logger.debug(datasets);
	}
	
	/**
	 * This method is used to retrieve an unsorted list with dataset names
	 * available in the service feed.
	 * @return ArrayList with available dataset names.
	 */
	public ArrayList getDatasetNames() {
		return datasetNames;
	}

	/**
	 * This method is used to retrieve a map with all datasets available 
	 * in the service feed.
	 * @return HashMap with available datasets.
	 */
	public HashMap getDatasets() {
		return datasets;
	}
	
	/**
	 * This method returns the url of the OpenSearch Description.
	 * @return String OpenSearch Description Url.
	 */
	public String getOpensearchDescriptionUrl() {
		return searchLink;
	}

	/**
	 * This method returns the url of the Service Metadata (ISO 19139).
	 * @return String Service Metadata Url.
	 */
	public String getServiceMetadataUrl() {
		return null;
	}
	
	public String getTitle() {
		return feedTitle;
	}
	
}
