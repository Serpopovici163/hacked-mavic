package com.example.hackedmavic;

import androidx.core.app.ActivityCompat;
import androidx.fragment.app.FragmentActivity;

import android.Manifest;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.text.InputType;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.example.hackedmavic.databinding.ActivityMapsBinding;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private ActivityMapsBinding binding;
    private Button sendButton;
    private Button paramButton;
    int altitude = 50; //standard alt of 50m
    LatLng user;
    LatLng drone = null;
    NetworkIO networkIO = new NetworkIO();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        networkIO.connectP2P();

        binding = ActivityMapsBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

        sendButton = binding.getRoot().findViewById(R.id.send_button);
        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //check if UAV position marker exists on map
                if (drone != null) {
                    int returnVal = networkIO.send(drone, altitude);
                    if (returnVal == NetworkIO.DUPLICATE_REQUEST)
                        toast("Duplicate request, not sent");
                    else if (returnVal == NetworkIO.PEER_OFFLINE)
                        toast("UAV offline");
                }
            }
        });

        paramButton = binding.getRoot().findViewById(R.id.param_button);
        paramButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AlertDialog.Builder builder = new AlertDialog.Builder(MapsActivity.this);
                builder.setTitle("Parameters");
                builder.setMessage("Altitude (m)");
                final EditText altitude_input = new EditText(MapsActivity.this);
                altitude_input.setInputType(InputType.TYPE_CLASS_NUMBER);
                builder.setView(altitude_input);

                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        String altitudeStr = altitude_input.getText().toString();
                        altitude = Integer.parseInt(altitudeStr);
                    }
                });
                builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });
                builder.show();
            }
        });
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {

        LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            return;
        }
        Location location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
        double longitude = location.getLongitude();
        double latitude = location.getLatitude();
        user = new LatLng(latitude, longitude);

        mMap = googleMap;
        mMap.setOnMapClickListener(new GoogleMap.OnMapClickListener() {
            @Override
            public void onMapClick(LatLng latLng) {
                drone = latLng;
                mMap.clear();
                mMap.addMarker(new MarkerOptions().position(user).title("You").icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN)));
                mMap.addMarker(new MarkerOptions().position(drone).title("Drone").icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED)));
            }
        });

        // Add a marker on user's location and move map
        mMap.addMarker(new MarkerOptions().position(user).title("You").icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN)));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(user));
    }

    public void toast(String message) {
        Toast.makeText(MapsActivity.this, message, Toast.LENGTH_LONG).show();
    }

}