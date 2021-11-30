package com.example.hackedmavic;

import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import com.google.android.gms.maps.model.LatLng;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.URL;
import java.util.Objects;

public class NetworkIO {

    static int DUPLICATE_REQUEST = 99;
    static int PEER_OFFLINE = 98;

    private String server="http://ludicroustech.ca";
    private int port = 55555;
    String peerIP = "";
    int peerSrcPort = 55555;
    int peerDstPort = 55556;
    LatLng prevDrone = null;

    void connectP2P() {
        new Thread() {
            @Override
            public void run() {
                try {
                    DatagramSocket ds = new DatagramSocket(port);
                    byte[] buf = "0".getBytes();
                    DatagramPacket dp = new DatagramPacket(buf, buf.length, InetAddress.getByName(new URL(server).getHost()), port);
                    ds.send(dp);
                    byte[] recvBuf = new byte[1024];
                    DatagramPacket recvPacket = new DatagramPacket(recvBuf, recvBuf.length);
                    ds.receive(recvPacket);
                    String recvStr = new String(recvPacket.getData(), 0, recvPacket.getLength());
                    if (Objects.equals(recvStr, "ready")) {
                        MapsActivity mapsActivity = new MapsActivity();
                        mapsActivity.toast("Waiting on drone");
                        //now wait for peer info
                        ds.receive(recvPacket);
                        recvStr = new String(recvPacket.getData(), 0, recvPacket.getLength());
                        Log.e("P2P", recvStr); //DEBUG
                        String[] data = recvStr.split(" ");
                        peerIP = data[0];
                        peerSrcPort = Integer.parseInt(data[1]);
                        peerDstPort = Integer.parseInt(data[2]);

                    }
                    ds.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }.start();
    }

    int send(LatLng drone, int altitude){
        //check for duplicate packet
        if (Objects.equals(drone, prevDrone))
            return DUPLICATE_REQUEST;

        //check if UAV is online
        if (Objects.equals(peerIP, ""))
            return PEER_OFFLINE;

        //request format is lat/lng/alt
        String request = String.valueOf(drone.latitude) + "/" + String.valueOf(drone.longitude) + "/" + String.valueOf(altitude);
        new Thread() {
            @Override
            public void run() {
                try {
                    DatagramSocket ds = new DatagramSocket(port);
                    byte[] buf = request.getBytes();
                    DatagramPacket dp = new DatagramPacket(buf, buf.length, InetAddress.getByName(peerIP), peerDstPort);
                    ds.send(dp);
                    byte[] recvBuf = new byte[1024];
                    DatagramPacket recvPacket = new DatagramPacket(recvBuf, recvBuf.length);
                    ds.receive(recvPacket);
                    String recvStr = new String(recvPacket.getData(), 0, recvPacket.getLength());
                    if (Objects.equals(recvStr, "ok")) {
                        MapsActivity mapsActivity = new MapsActivity();
                        mapsActivity.toast("Response OK");
                    }
                    ds.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }.start();

        return 0;
    }
}
