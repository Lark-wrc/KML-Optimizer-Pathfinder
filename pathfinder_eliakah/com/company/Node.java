package com.company;

import java.util.ArrayList;

/**
 * Created by Research on 4/7/2016.
 */
public  class Node {
    Point point;
    ArrayList<Node> edges = new ArrayList<Node>();
    public Node(){

    }
    public Node(Point point){
        this.point = point;
    }

    Point coordinates(){
        return point;
    }

    void addEdge( Node n){
        edges.add(n);
    }

    ArrayList<Node> edges(){
        return edges;
    }

}