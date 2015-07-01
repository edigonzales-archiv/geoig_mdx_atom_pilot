package org.catais.inspire.dls;

import java.util.Date;
import java.util.List;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.rometools.modules.georss.GeoRSSModule;
import com.rometools.modules.georss.GeoRSSUtils;
import com.rometools.rome.feed.synd.SyndEntry;
import com.rometools.rome.feed.synd.SyndLink;

public class DatasetFeedEntry {
	static final Logger logger = LogManager.getLogger(DatasetFeedEntry.class.getName());

	private String title;
	private String summary;
	private String uri; // equal to alternate link?
	private Date updated;
	private String datasetAlternativeLink;
	private String mimeType;
	private String crs;

	public DatasetFeedEntry(SyndEntry entry) {
        title = entry.getTitle();
        summary = entry.getDescription().getValue();
        uri = entry.getUri();
        updated = entry.getUpdatedDate();
        
        // link to dataset
        List<SyndLink> links = entry.getLinks();
        for (SyndLink link: links) {
        	String rel = link.getRel();
        	
        	if (rel.equalsIgnoreCase("alternate")) {
        		datasetAlternativeLink = link.getHref();
        		mimeType = link.getType();
        	}   
        }
        
        // there can be only one crs
        crs = entry.getCategories().get(0).getName();
        
        // do something with the geometry
        GeoRSSModule geoRSSModule = GeoRSSUtils.getGeoRSS(entry);
        com.rometools.modules.georss.geometries.AbstractGeometry geom = geoRSSModule.getGeometry();
        
        if (geom instanceof com.rometools.modules.georss.geometries.Envelope)
        	logger.trace("I'm an Envelope");
	}
	
	public String getTitle() {
		return title;
	}
	
	public String getSummary() {
		return summary;
	}
	
	public Date getUpdateDate() {
		return updated;
	}
	
	public String getDatasetAlternativeLink() {
		return datasetAlternativeLink;
	}

	public String getMimeType() {
		return mimeType;
	}
	
	public String getCRS() {
		return crs;
	}
		
}
