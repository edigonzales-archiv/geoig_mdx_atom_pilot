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

public class ServiceFeed {
	static final Logger logger = LogManager.getLogger(ServiceFeed.class.getName());
	
	private String serviceFeedUrl;
	
	private ArrayList<String> datasetNames = new ArrayList<String>();
	private ArrayList<ServiceFeedEntry> datasets = new ArrayList<ServiceFeedEntry>();
	private String feedTitle;
	private Date updated;
	private String serviceFeedLink;
	private String serviceFeedDescriptionLink;
	private String opensearchDescriptionLink;

	public ServiceFeed(String serviceFeedUrl) throws MalformedURLException, IOException, FeedException {
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
        		serviceFeedLink = link.getHref();
        	} else if (rel.equalsIgnoreCase("describeby")) {
        		serviceFeedDescriptionLink = link.getHref();
        	} else if (rel.equalsIgnoreCase("search")) {
        		opensearchDescriptionLink = link.getHref();
        	}
        }  
    	
    	// get all service feed entries
    	List<SyndEntry> entries = feed.getEntries();
    	for (SyndEntry entry: entries) {    		
    		ServiceFeedEntry sfe = new ServiceFeedEntry(entry);
    		datasets.add(sfe);   
    		datasetNames.add(sfe.getTitle());
    	}
	}
	
	// Do I need this?
	// ServiceFeed returns everything I need to know to deal with DatasetFeed.
	public ArrayList getDatasetAlternatives(String code, String namespace) throws MalformedURLException, IOException, FeedException {
		for (ServiceFeedEntry sfe : datasets) {
			String sfeCode = sfe.getSpatialDatasetIdentifierCode();
			String sfeNamespace = sfe.getSpatialDatasetIdentifierNamespace();
			
			if (sfeCode.equalsIgnoreCase(code) && sfeNamespace.equalsIgnoreCase(namespace)) {
				DatasetFeed dsf = new DatasetFeed(sfe.getDatasetFeedLink());
				return dsf.getDatasetAlternatives();
			}
			// code AND namespace not found
			return new ArrayList();
		}
		// no entries in servicefeed
		return new ArrayList();
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
	public ArrayList getDatasets() {
		return datasets;
	}
	
	/**
	 * This method returns the url of the OpenSearch Description.
	 * @return String OpenSearch Description Url.
	 */
	public String getOpensearchDescriptionLink() {
		return opensearchDescriptionLink;
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
