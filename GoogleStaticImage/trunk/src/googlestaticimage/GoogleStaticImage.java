package googlestaticimage;

import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.Authenticator;
import java.net.PasswordAuthentication;
import java.net.URL;
import java.util.Properties;
import javax.imageio.ImageIO;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPathExpressionException;
import org.xml.sax.SAXException;

public class GoogleStaticImage {

    public static void getImage(Properties props) throws IOException, InterruptedException {

        String imgDir = props.getProperty("imageDir");
        int startRow = Integer.parseInt(props.getProperty("startRow"));
        int startCol = Integer.parseInt(props.getProperty("startCol"));
        int totalRows = Integer.parseInt(props.getProperty("totalRows"));
        int totalCols = Integer.parseInt(props.getProperty("totalCols"));
        double startLat = Double.parseDouble(props.getProperty("startLat"));
        double startLon = Double.parseDouble(props.getProperty("startLon"));
        double deltaLat = Double.parseDouble(props.getProperty("deltaLat"));
        double deltaLon = Double.parseDouble(props.getProperty("deltaLon"));
        int zoom = Integer.parseInt(props.getProperty("zoom"));
        int scale = Integer.parseInt(props.getProperty("scale"));
        String format = props.getProperty("format");
        String size = props.getProperty("size");
        int sleep = Integer.parseInt(props.getProperty("sleep"));
        String key = props.getProperty("key");
        System.out.println("Start lat, lon: " + startLat + ", " + startLon);
        System.out.println("Delta lat: " + deltaLat);
        System.out.println("Delta lon: " + deltaLon);
        System.out.println("Start row, col: " + startRow + ", " + startCol);
        System.out.println("Total row, col: " + totalRows + ", " + totalCols);
        System.out.println("Zoom, scale, format, size: " + zoom + ", " + scale + ", " + format + ", " + size);
        double lat = startLat;
        for (int i = 0; i < totalRows; i++) {
            double lon = startLon;
            if (i >= startRow) {
                for (int j = 0; j < totalCols; j++) {
                    if (i == startRow && j < startCol) {
                        lon += deltaLon;
                        System.out.println("gone");
                        continue;
                    }
                    String query = "http://maps.googleapis.com/maps/api/staticmap?center=" + lat + "," + lon + "&zoom=" + zoom + "&size=" + size + "&scale=" + scale + "&format=" + format + "&maptype=satellite&sensor=false&key=" + key;
                    System.out.println(query);
                    BufferedImage bi = ImageIO.read(new URL(query));
                    String imageFilename = imgDir + "image" + i + "-" + j + ".png";
                    File imageFile = new File(imageFilename);
                    ImageIO.write(bi, "png", imageFile);
                    String msg = lat + ", " + lon + ", " + query + ", " + imageFilename + "**\n";
                    System.out.print(msg);
                    Thread.currentThread().sleep(sleep);
                    System.out.println(lat + "," + lon);
                    lon += deltaLon;
                }
            }
            lat -= deltaLat;

        }
    }
    public static void main(String args[]) throws XPathExpressionException, ParserConfigurationException, SAXException, FileNotFoundException, IOException, InterruptedException {
        Properties props = new Properties();
        props.load(new FileInputStream("image.properties"));
        final String proxyHost = props.getProperty("proxyHost");
        final String proxyPort = props.getProperty("proxyPort");
        final String userName = props.getProperty("userName");
        final String passwd = props.getProperty("passwd");
        if (proxyHost != null && proxyPort != null && userName != null && passwd != null) {
            System.setProperty("http.proxyHost", "proxy.tcs.com");
            System.setProperty("http.proxyPort", "8080");
            Authenticator.setDefault(new Authenticator() {
                @Override
                protected PasswordAuthentication getPasswordAuthentication() {
                    return new PasswordAuthentication(userName, passwd.toCharArray());
                }
            });
        }
        System.out.println(props.getProperty("imageDir"));
        getImage(props);
    }
}
