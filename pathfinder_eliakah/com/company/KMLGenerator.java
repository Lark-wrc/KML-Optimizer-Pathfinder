package com.company;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Date;

/**
 * Created by Research on 4/21/2016.
 */
public class KMLGenerator {

        ArrayList<Node> nodes ;
        ArrayList<Point> path ;

    public  KMLGenerator (ArrayList<Node> nodes ,ArrayList<Point> path){
        this.nodes = nodes;
        this.path = path;
    }

         void generate() throws IOException {
            //creates file
            String filename = (getFileName());
            File outPutFile = new File(filename);

            if (outPutFile.createNewFile()) {
                String text = "";
                PrintWriter writer = new PrintWriter(filename, "UTF-8");
                writer.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n <kml xmlns=\"http://www.opengis.net/kml/2.2\">\n");
               // writer.write(" <Document>\n<name>"+filename+"</name> \n");

                //writting graph
                 //   writer.write(createGraph());

                //writting placemarks
               // for (int i = 0; i < edges.size(); i++) {

                   // writer.write(createPlacemark());


               // }


              //  writer.write("</Document>\n");
                String tag = "  <Document>\n" +
                        "    <name>Paths</name>\n" +
                        "    <description>Examples of paths. Note that the tessellate tag is by default\n" +
                        "      set to 0. If you want to create tessellated lines, they must be authored\n" +
                        "      (or edited) directly in KML.</description>\n" +
                        "    <Style id=\"yellowLineGreenPoly\">\n" +
                        "      <LineStyle>\n" +
                        "        <color>7f00ffff</color>\n" +
                        "        <width>4</width>\n" +
                        "      </LineStyle>\n" +
                        "      <PolyStyle>\n" +
                        "        <color>7f00ff00</color>\n" +
                        "      </PolyStyle>\n" +
                        "    </Style>\n"+
                "    <Style id=\"blueLineGreenPoly\">\n" +
                        "      <LineStyle>\n" +
                        "        <color>ffFF0000</color>\n" +
                        "        <width>4</width>\n" +
                        "      </LineStyle>\n" +
                        "      <PolyStyle>\n" +
                        "        <color>ffFF0000</color>\n" +
                        "      </PolyStyle>\n" +
                        "    </Style>\n";
                writer.write(tag);

                for (int i = 0; i <nodes.size() ; i++) {
                    writer.write(createPath(nodes.get(i)));
                   // System.out.println(createPath(nodes.get(i)));
                }

                    writer.write(createKMainPath(path));
                   // System.out.println(createPath(nodes.get(i)));


                writer.write("</Document>\n</kml>");
                writer.close();
            } else {
                System.out.println("File Creation Unsuccessful!.");
            }
        }


        public String createPlacemark() {
            String tag = "";

            for (int i = 0; i < nodes.size(); i++) {

                tag += "<Placemark>\n<name>" + nodes.get(i).point.getLatitude()+","+nodes.get(i).point.getLongitude()+ "</name>\n";
                tag += "<description>sample description</description>\n<Point>\n<coordinates>" +  nodes.get(i).point.getLatitude()+","+nodes.get(i).point.getLongitude()+"\n";
                tag += "</coordinates>\n</Point>\n</Placemark>\n";
            }
            return tag;
        }

    public String createPath(Node n) {

        String tag = "";


            for (int i = 0; i < n.edges.size(); i++) {

                tag += "    <Placemark>\n" +
                        "      <name>Absolute Extruded</name>\n" +
                        "      <description>Transparent green wall with yellow outlines</description>\n" +
                        "      <styleUrl>#yellowLineGreenPoly</styleUrl>\n" +
                        "      <LineString>\n" +
                        "        <extrude>1</extrude>\n" +
                        "        <tessellate>1</tessellate>\n" +
                        "        <altitudeMode>absolute</altitudeMode>\n" +
                        "        <coordinates>";
                tag +=  n.point.getLatitude() + "," + n.point.getLongitude() + "\n";
                tag += n.edges.get(i).point.getLatitude() + "," + n.edges.get(i).point.getLongitude() + "\n";
                tag += "  </coordinates>\n" +
                        "      </LineString>\n" +
                        "    </Placemark>\n";

            }



        return tag;
    }

public String createKMainPath(ArrayList<Point> n) {

        String tag = "";
                tag += "<Placemark>\n" +
                        "      <name>Absolute Extruded</name>\n" +
                        "      <description>Transparent green wall with yellow outlines</description>\n" +
                        "      <styleUrl>#blueLineGreenPoly</styleUrl>\n" +
                        "      <LineString>\n" +
                        "        <extrude>1</extrude>\n" +
                        "        <tessellate>1</tessellate>\n" +
                        "        <altitudeMode>absolute</altitudeMode>\n" +
                        "        <coordinates>\n";
    for (int i = 0; i < n.size(); i++) {
                        tag+=  n.get(i).getLatitude() + "," + n.get(i).getLongitude() + "\n";
    }
                      tag+=  "        </coordinates>\n" +
                        "      </LineString>\n" +
                        "    </Placemark>";
        return tag;
    }



        private String getFileName(){
            Date date = new Date();
            String timeStamp = ""+date;
            timeStamp = timeStamp.replaceAll(" ", "_").toLowerCase();
            timeStamp = timeStamp.replaceAll(":", "_").toLowerCase();
            timeStamp += timeStamp+".kml";
            return timeStamp;
        }



}
