package com.company;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Created by eliakah on 3/31/2016.
 */
public class GraphGenerator {

    double lat1 ,long1, lat2,  long2 ;
    ArrayList<Point> points  = new ArrayList<Point>();
    Graph graph = new Graph();
    int distance = 20;
    double minDistance;
    public GraphGenerator(){

    }
    public GraphGenerator(double  lat1 , double long1, double lat2, double long2 ){
        this.lat1 = lat1;
        this.lat2 = lat2;
        this.long1 = long1;
        this.long2 = long2;

    }
    public GraphGenerator(double  lat1 , double long1, double lat2, double long2 , int distance){
        this.lat1 = lat1;
        this.lat1 = lat2;
        this.long1 = long1;
        this.long2 = long2;
        this.distance = distance;
    }

    public ArrayList<Point> getPoints  () throws IOException {
        double x, y;
        int flag;
        PixelChecker checker = new PixelChecker();
        for (x = lat1; x > lat2; x--) {
            for (y = long1; y < long2; y++) {
               flag = checker.execute(x,y);
               if (flag == 0 ){
                    points.add(new Point(y, x));
                    System.out.println(flag +" | " + x + ", " + y);
                }
            }
        }

        minDistance = getDistance(points.get(1), points.get(2));

     return points;

    }

    ArrayList<Node> genGraph(){
        ArrayList<Node> nodes = new ArrayList<Node>();
        Node current;
        for (int i = 0; i < points.size(); i++) {
            nodes.add(new Node(points.get(i)));
        }


        for (int i = 0; i < nodes.size(); i++) {
            current = nodes.get(i);
            for (int j = 0; j < nodes.size() ; j++) {
                if((current.point != nodes.get(j).point)) {
                    if((getDistance(current.point, nodes.get(j).point) <= minDistance) && (current.point.latitude <= nodes.get(j).point.latitude) &&(current.point.longitude <= nodes.get(j).point.longitude) )
                    current.addEdge(nodes.get(j));
               }
            }
            //nodes.add(current);
        }


        return nodes;
    }


    private Double  getDistance(Point one, Point two){
        double R = 6371000; // metres
        double lat1 = (one.getLatitude()*Math.PI)/180; // convert to toRadians
        double lat2 = (two.getLatitude()*Math.PI)/180; // convert to toRadians
        double latDiff = ((two.getLatitude()-one.getLatitude())*Math.PI)/180; // convert to toRadians
        double longDiff = ((two.getLongitude()-one.getLongitude())*Math.PI)/180; // convert to toRadians

        double a = Math.sin(latDiff/2) * Math.sin(latDiff/2) +
                Math.cos(lat1) * Math.cos(lat2) *
                        Math.sin(longDiff/2) * Math.sin(longDiff/2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

        double d = R * c;
        return d;
    }
}

