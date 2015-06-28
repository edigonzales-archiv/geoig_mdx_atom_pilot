package org.catais.geoig.ai;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class MetaDb {
	static final Logger logger = LogManager.getLogger(MetaDb.class.getName());
	private static Connection connection;

	public MetaDb(String metadbPath) throws ClassNotFoundException, SQLException {
		Class.forName("org.sqlite.JDBC");
		
		connection = DriverManager.getConnection("jdbc:sqlite:" + metadbPath);
        logger.debug("Connection closed: " + connection.isClosed());
	}
	
	@SuppressWarnings("unchecked") 
	public ArrayList getEntries() throws SQLException, ParseException {
		HashMap entry = new HashMap();
		ArrayList<HashMap> entries = new ArrayList();
		
		Statement stmt = connection.createStatement(); 
		String sql = "SELECT * FROM amtliche_vermessung;";
		
		ResultSet rs = stmt.executeQuery(sql);
		while (rs.next()) {
			entry.put("pkuid", rs.getInt("pkuid"));
			entry.put("bfsnr", rs.getInt("bfsnr"));
			entry.put("canton", rs.getString("canton"));
			entry.put("gem_name", rs.getString("gem_name"));
			
			DateFormat df = new SimpleDateFormat("yyyy-MM-dd H:m:s");
			entry.put("updated", df.parse(rs.getString("updated")));
			entry.put("imported", df.parse(rs.getString("imported")));
			
			entry.put("spatial_dataset_identifier_code", rs.getString("spatial_dataset_identifier_code"));
			entry.put("spatial_dataset_identifier_namespace", rs.getString("spatial_dataset_identifier_namespace"));
			entry.put("mime_type", rs.getString("mime_type"));
			entry.put("crs", rs.getString("crs"));
			entry.put("service_feed", rs.getString("service_feed"));
			entry.put("path", rs.getString("path"));
			entries.add(entry);	
			logger.debug(entry);
		}
		return entries;
	}
	
	public void shutdown() {
		try {
			if(connection != null) {
				connection.close();
			}
		} catch (SQLException e) {
			e.printStackTrace();
			logger.error(e.getMessage());
		}
	}
	

}
