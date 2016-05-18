package com.company;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

/**
 * Created by eliakah on 3/31/2016.
 */
public class PixelChecker {
    public int execute(double lat, double lng) throws IOException {
        URL link = new URL("http://localhost/PointChecker/src/com/company/index.php?latLong="+lat+","+lng);
        URLConnection connection = link.openConnection();
        BufferedReader in = new BufferedReader(
                new InputStreamReader(
                        connection.getInputStream()));
        String inputLine;

        while ((inputLine = in.readLine()) != null)
            return Integer.parseInt(inputLine);
        in.close();
        return 0;
    }
}
