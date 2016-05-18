package com.company;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by eliakah on 3/31/2016.
 */

public class Point {
    Map<Point, Double> edges = new HashMap<>();
    double latitude, longitude;
    String description;
    Point(double latitude, double longitude){
        this.latitude = latitude;
        this.longitude = longitude;
    }
    Point(double latitude, double longitude, String description){
        this.latitude = latitude;
        this.longitude = longitude;
        this.description = description;
    }


    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public String getDescription(){
        return description;
    }


    public void addEdge(Point p, double w){
        if(!edges.containsKey(p)){
            edges.put(p,w );
            p.addEdge(new Point(latitude, longitude), w);
        }

    }
    public Map<Point, Double> getEdges(){
        return  edges;
    }


}
