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
    int peerSrcPort = 0;
    int peerDstPort = 0;
    LatLng prevDrone = null;

    Context mCont;

    public NetworkIO(Context context) {
        mCont = context;
    }

    void connectP2P() {
        new Thread() {
            @Override
            public void run() {
                try {
                    DatagramSocket ds = new DatagramSocket(50001);
                    byte[] buf = "0".getBytes();
                    DatagramPacket dp = new DatagramPacket(buf, buf.length, InetAddress.getByName(new URL(server).getHost()), port);
                    ds.send(dp);
                    byte[] recvBuf = new byte[1024];
                    DatagramPacket recvPacket = new DatagramPacket(recvBuf, recvBuf.length);
                    ds.receive(recvPacket);
                    String recvStr = new String(recvPacket.getData(), 0, recvPacket.getLength());
                    Log.e("P2P", recvStr); //DEBUG
                    if (Objects.equals(recvStr, "ready")) {
                        //Toast.makeText(mCont, "Waiting on drone", Toast.LENGTH_LONG).show();
                        //now wait for peer info
                        ds.receive(recvPacket);
                        recvStr = new String(recvPacket.getData(), 0, recvPacket.getLength());
                        Log.e("P2P", recvStr); //DEBUG
                        String[] data = recvStr.split(" ");
                        peerIP = data[0];
                        peerSrcPort = Integer.parseInt(data[1]);
                        peerDstPort = Integer.parseInt(data[2]);
                        Log.e("P2P", "IP: " + peerIP);
                        Log.e("P2P", "SPORT: " + String.valueOf(peerSrcPort));
                        Log.e("P2P", "DPORT: " + String.valueOf(peerDstPort));
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
                    DatagramSocket ds = new DatagramSocket(peerDstPort);
                    byte[] buf = request.getBytes();
                    DatagramPacket dp = new DatagramPacket(buf, buf.length, InetAddress.getByName(peerIP), peerSrcPort);
                    Log.e("SEND", "presend");
                    ds.send(dp);
/*                    byte[] recvBuf = new byte[1024];
                    DatagramPacket recvPacket = new DatagramPacket(recvBuf, recvBuf.length);
                    ds.receive(recvPacket);
                    String recvStr = new String(recvPacket.getData(), 0, recvPacket.getLength());
                    if (Objects.equals(recvStr, "ok")) {
                        MapsActivity mapsActivity = new MapsActivity();
                        mapsActivity.toast("Response OK");
                    }*/
                    ds.close();
                    Log.e("SEND", "done");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }.start();

        prevDrone = drone;

        return 0;
    }
}
