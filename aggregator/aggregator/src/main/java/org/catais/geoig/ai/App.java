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
import org.catais.inspire.dls.DownloadService;
import org.catais.inspire.dls.OpenSearchDescription;

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
        	
        	DownloadService dls = new DownloadService("http://www.catais.org/geoig/services/dls/ch/so/agi/service.xml");
//        	DownloadService dls = new DownloadService("http://www.weichand.de/inspire/dls/verwaltungsgrenzen.xml");
        	
        	String osdUrl = dls.getOpensearchDescriptionUrl();
        	
        	
//        	logger.debug("Feed Title: " + dls.getTitle());
//        	logger.debug("Dataset Names: " + dls.getDatasetNames());
        	
        	OpenSearchDescription osd = new OpenSearchDescription(osdUrl);
        	
        	
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
