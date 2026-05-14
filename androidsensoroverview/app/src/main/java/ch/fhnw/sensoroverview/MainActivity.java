package ch.fhnw.sensoroverview;

import android.app.ActivityManager;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.os.Build;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.List;

public class MainActivity extends AppCompatActivity {

    private SensorManager sensorManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        populateDeviceInfo();
        populateSensorList();
    }

    private void populateDeviceInfo() {
        ((TextView) findViewById(R.id.device_manufacturer))
                .setText("Manufacturer: " + Build.MANUFACTURER);
        ((TextView) findViewById(R.id.device_model))
                .setText("Model: " + Build.MODEL);
        ((TextView) findViewById(R.id.device_android_version))
                .setText("Android Version: " + Build.VERSION.RELEASE);
        ((TextView) findViewById(R.id.device_api_level))
                .setText("API Level: " + Build.VERSION.SDK_INT);

        DisplayMetrics dm = getResources().getDisplayMetrics();
        ((TextView) findViewById(R.id.device_screen_resolution))
                .setText("Screen Resolution: " + dm.widthPixels + " x " + dm.heightPixels + " px");
        ((TextView) findViewById(R.id.device_screen_density))
                .setText("Screen Density: " + dm.densityDpi + " dpi");

        ActivityManager.MemoryInfo memInfo = new ActivityManager.MemoryInfo();
        ((ActivityManager) getSystemService(Context.ACTIVITY_SERVICE)).getMemoryInfo(memInfo);
        long totalRamMb = memInfo.totalMem / (1024 * 1024);
        ((TextView) findViewById(R.id.device_total_ram))
                .setText("Total RAM: " + totalRamMb + " MB");
    }

    private void populateSensorList() {
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        List<Sensor> sensorList = sensorManager.getSensorList(Sensor.TYPE_ALL);

        StringBuilder sensorText = new StringBuilder();
        for (Sensor current : sensorList) {
            sensorText.append(current.getName()).append(System.getProperty("line.separator"));
        }

        ((TextView) findViewById(R.id.sensorlist)).setText(sensorText);
    }
}