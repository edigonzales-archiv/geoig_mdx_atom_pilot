package org.catais.geoig.ai;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.sql.SQLException;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Date;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.catais.inspire.dls.DatasetFeed;
import org.catais.inspire.dls.DatasetFeedEntry;
import org.catais.inspire.dls.ServiceFeed;
import org.catais.inspire.dls.OpenSearchDescription;
import org.catais.inspire.dls.ServiceFeedEntry;

import com.rometools.rome.feed.synd.SyndFeed;
import com.rometools.rome.io.FeedException;
import com.rometools.rome.io.SyndFeedInput;
import com.rometools.rome.io.XmlReader;

public class App 
{
	static final Logger logger = LogManager.getLogger(App.class.getName());
	
	// TEMP
	static final String metadbPath = "/Users/stefan/Projekte/geoig_mdx_atom_pilot/aggregator/sqlite_db/amtliche_vermessung.sqlite";
	
    public static void main( String[] args )
    {
    	logger.info("Start: "+ new Date());
    	
    	try {
        	MetaDb metadb = new MetaDb(metadbPath);
        	ArrayList entries = metadb.getEntries();
        	metadb.shutdown(); // Shutdown after download etc. since we need to update the dates.
        	
        	ServiceFeed sf = new ServiceFeed("http://www.catais.org/geoig/services/dls/ch/gl/service.xml");
        	
        	// Wrap this in a class called 'DownloadService'...

        	// returns opensearch description of service feed
        	String osdl = sf.getOpensearchDescriptionLink();
        	logger.debug(osdl);
        	
        	// this returns the first servicefeed entry = 'dataset'
        	String code = ((ServiceFeedEntry)sf.getDatasets().get(0)).getSpatialDatasetIdentifierCode();
        	String namespace = ((ServiceFeedEntry)sf.getDatasets().get(0)).getSpatialDatasetIdentifierNamespace();
        	String datasetFeedUrl = ((ServiceFeedEntry)sf.getDatasets().get(0)).getDatasetFeedLink();

        	// now we want to know what dataset alternatives exists
        	DatasetFeed df = new DatasetFeed(datasetFeedUrl);
        	ArrayList<DatasetFeedEntry> datasetAlternatives = df.getDatasetAlternatives();
        	
        	for (DatasetFeedEntry datasetAlternative : datasetAlternatives) {
        		logger.debug(datasetAlternative.getDatasetAlternativeLink());        		
        		logger.debug(datasetAlternative.getMimeType());        		
        	}
        	
    	} catch (ClassNotFoundException e) {
    		e.printStackTrace();
    		logger.error(e.getMessage());
    	} catch (SQLException e) {
    		e.printStackTrace();
    		logger.error(e.getMessage());
    	} catch (ParseException e) {
    		e.printStackTrace();
    		logger.error(e.getMessage());
    	} catch (MalformedURLException e) {
    		e.printStackTrace();
    		logger.error(e.getMessage());
    	} catch (IOException e) {
    		e.printStackTrace();
    		logger.error(e.getMessage());
    	} catch (FeedException e) {
    		e.printStackTrace();
    		logger.error(e.getMessage());
    	}
    	logger.info("Stop: "+ new Date());
    }
}
