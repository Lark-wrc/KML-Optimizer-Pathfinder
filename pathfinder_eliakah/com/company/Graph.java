package com.company;

import java.util.ArrayList;

/**
 * Created by Research on 4/7/2016.
 */
public class Graph {

    ArrayList<Node> graph = new ArrayList<>();
    public Graph() {
    }
    public Graph(ArrayList<Node> graph) {
        this.graph = graph;
    }

    void addNode(Node n){
        graph.add(n);
    }

    ArrayList<Node> graph (){
        return graph;
    }


}

