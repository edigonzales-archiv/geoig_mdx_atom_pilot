package org.catais.inspire.dls;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.rometools.modules.georss.GeoRSSModule;
import com.rometools.modules.georss.GeoRSSUtils;
import com.rometools.rome.feed.synd.SyndCategory;
import com.rometools.rome.feed.synd.SyndEntry;
import com.rometools.rome.feed.synd.SyndLink;

import de.weichand.inspire.inspirerome.InspireDlsModule;
import de.weichand.inspire.inspirerome.InspireDlsModuleImpl;

public class ServiceFeedEntry {
	static final Logger logger = LogManager.getLogger(ServiceFeedEntry.class.getName());
	
	private String title;
	private String summary;
	private String uri; // equal to alternate link?
	private Date updated;
	private String datasetFeedLink;
	private String datasetDescriptionLink;
	private ArrayList<String> crs = new ArrayList<String>();
	private String spatialDatasetIdentifierCode;
	private String spatialDatasetIdentifierNamespace;
	
	public ServiceFeedEntry(SyndEntry entry) {        
        title = entry.getTitle();
        summary = entry.getDescription().getValue();
        uri = entry.getUri();
        updated = entry.getUpdatedDate();
        
        // link to dataset feed and metadata
        List<SyndLink> links = entry.getLinks();
        for (SyndLink link: links) {
        	String rel = link.getRel();
        	
        	if (rel.equalsIgnoreCase("alternate")) {
        		datasetFeedLink = link.getHref();
        	} else if (rel.equalsIgnoreCase("describeby")) {
        		datasetDescriptionLink = link.getHref();
        	}
        }   
        
        // available crs
        List<SyndCategory> categories = entry.getCategories();
        for (SyndCategory category: categories) {
        	crs.add(category.getName());
        }
       
        // additional inspire stuff (rome inspire module from weichand.de is needed)
        InspireDlsModule inspireDlsModule = (InspireDlsModuleImpl) entry.getModule(InspireDlsModule.URI);
        spatialDatasetIdentifierCode = inspireDlsModule.getSpatialDatasetIdentifier().getCode();
        spatialDatasetIdentifierNamespace = inspireDlsModule.getSpatialDatasetIdentifier().getNamespace();
                
        // do something with the geometry, e.g. convert it to a jts geometry
        GeoRSSModule geoRSSModule = GeoRSSUtils.getGeoRSS(entry);
        com.rometools.modules.georss.geometries.AbstractGeometry geom = geoRSSModule.getGeometry();
        
        if (geom instanceof com.rometools.modules.georss.geometries.Envelope)
        	logger.trace("I'm an Envelope");
	}
	
	public String getTitle() {
		return title;
	}
	
	public String getSpatialDatasetIdentifierCode() {
		return spatialDatasetIdentifierCode;
	}
	
	public String getSpatialDatasetIdentifierNamespace() {
		return spatialDatasetIdentifierNamespace;
	}
	
	public String getDatasetFeedLink() {
		return datasetFeedLink;
	}

}
