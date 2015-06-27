package org.catais.geoig.ai;

import java.sql.SQLException;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Date;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

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
        	
        	
        	
        	
        	

    		
    	} catch (ClassNotFoundException e) {
    		e.printStackTrace();
    		logger.error(e.getMessage());
    	} catch (SQLException e)
    	{
    		e.printStackTrace();
    		logger.error(e.getMessage());
    	} catch (ParseException e)
    	{
    		e.printStackTrace();
    		logger.error(e.getMessage());
    	}
    	logger.info("Stop: "+ new Date());
    }
}
