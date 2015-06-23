package org.catais.geoig.ai;

import java.util.Date;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class App 
{
	static final Logger logger = LogManager.getLogger(App.class.getName());
	
    public static void main( String[] args )
    {
    	logger.info("Start: "+ new Date());
    	
    	MetaDb metadb = new MetaDb();
    	
    	
    	
    	
    	
    	logger.info("Stop: "+ new Date());
    }
}
