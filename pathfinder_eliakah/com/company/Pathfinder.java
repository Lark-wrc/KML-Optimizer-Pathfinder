package com.company;

import javax.print.DocFlavor;
import java.util.ArrayList;

/**
 * Created by Research on 5/16/2016.
 */
public class Pathfinder {
    ArrayList<Node> nodes ;
    Point start;
    Point end;


    public Pathfinder(ArrayList<Node> nodes){
        this.nodes = nodes;
        start = nodes.get(0).point;
        end = nodes.get(nodes.size() - 1).point;
    }

    public  ArrayList<Point> find(){
        ArrayList<Point> points = new  ArrayList<>();
        Node current = nodes.get(0);
        points.add(start);
      //  for (int i = 0; i < nodes.size(); i++) {
       //     current = nodes.get(i);
            while(current.edges.size() != 0) {
                Node shortest = getShortest(current.edges);
                points.add(shortest.point);
                current = shortest;
            }

       // }

        points.add(end);

        return points;
    }

    private Node getShortest(ArrayList<Node> points){
        Node p = points.get(0);
        double distance = getDistance(start, end);
        double temp;
        Node current;

        for (int i = 0; i <points.size() ; i++) {
            current = points.get(i);
            temp = getDistance(current.point, end);
            if(temp < distance ){
                distance = temp;
                p = current;
            }
        }



        return p;
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
