package com.company;

import java.io.IOException;
import java.util.ArrayList;

public class Main {

    public static void main(String[] args) throws IOException {
        // write your code here

        GraphGenerator gen = new GraphGenerator(17.549772, -26.367188,0.252685, 3.515625 );
        gen.getPoints();
        ArrayList<Node> nodes = gen.genGraph();
        Pathfinder finder = new Pathfinder(nodes);
       KMLGenerator k = new KMLGenerator(nodes, finder.find());
        k.generate();

        /*
        PixelChecker p = new PixelChecker();
        int flag = p.execute(22.177232, -3.164063);
        if (flag == 1 ){
            System.out.print("on Land");
        }else{
            System.out.print("NO Land");
        }*/

    }
}
