package org.catais.inspire.dls;

import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;

import javax.xml.XMLConstants;
import javax.xml.bind.JAXBContext;
import javax.xml.validation.SchemaFactory;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;



public class OpenSearchDescription {
	static final Logger logger = LogManager.getLogger(OpenSearchDescription.class.getName());
	
	String openSearchDescriptionUrl;

	public OpenSearchDescription(String openSearchDescriptionUrl) throws MalformedURLException, IOException  {
        this.openSearchDescriptionUrl = openSearchDescriptionUrl; 
        logger.debug(openSearchDescriptionUrl);
        
        InputStream is = new URL(openSearchDescriptionUrl).openStream();

        SchemaFactory schemaFactory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
        Schema        schema        = ( xsdSchema == null || xsdSchema.trim().length() == 0 )
                                      ? null : schemaFactory.newSchema( new File( xsdSchema ) );
        JAXBContext   jaxbContext   = JAXBContext.newInstance( jaxbElement.getClass().getPackage().getName() );        
        

        
        

	}

}
