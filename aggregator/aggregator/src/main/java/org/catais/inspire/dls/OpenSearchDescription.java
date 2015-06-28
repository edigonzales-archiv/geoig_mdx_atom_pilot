package org.catais.inspire.dls;

import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;

import javax.xml.XMLConstants;
import javax.xml.bind.JAXBContext;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;



public class OpenSearchDescription {
	static final Logger logger = LogManager.getLogger(OpenSearchDescription.class.getName());
	
	String openSearchDescriptionUrl;

	public OpenSearchDescription(String openSearchDescriptionUrl) throws MalformedURLException, IOException  {
        this.openSearchDescriptionUrl = openSearchDescriptionUrl; 
        logger.debug(openSearchDescriptionUrl);
        
        

        
        

	}

}
