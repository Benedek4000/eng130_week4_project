# Steps for Mobile App Setup

In Android studio

- Select a new project.
- Select "Empty Activity" template.

- Name the application
- Select the language as Java.

Once the project is open, we will have 2 files
1. `activity_main.xml` - This file contains all the design layout for the applicatoin.

- It already has prepopulated code for a constraint layout, but we will be using a `RelativeLayout` for the web view. 
- We will also need the Web View to be full screen, so we change its layout to `match_parent`.

**Note**: Don't forget to give an id for the WebView, else we won't be able to access it while writing the Java code.


The code for this file will look like:

```
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    
    <WebView
        android:id="@+id/webView"
        android:layout_width="match_parent"
        android:layout_height="match_parent">
        
    </WebView>
</RelativeLayout>
```


2. `MainActivity.java` - This file include all the code required to convert the web app to the mobile app.

```
package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.app.Activity;![MicrosoftTeams-image](https://user-images.githubusercontent.com/110366380/198543381-b0f8d154-75a3-438f-bcb6-2f765e85204e.png)

import android.os.Bundle;
import android.view.KeyEvent;
import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends AppCompatActivity {
    private WebView webView;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        CustomWebViewClient client =new CustomWebViewClient(this);
        webView = findViewById(R.id.webView);
        webView.setWebViewClient(client);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.loadUrl("https://www.quora.com/");

    }
    @Override
    public boolean onKeyDown(int keyCode,KeyEvent event ){
        if(keyCode== KeyEvent.KEYCODE_BACK && this.webView.canGoBack()){
            this.webView.goBack();
            return  true;
        }
        return super.onKeyDown(keyCode, event);
    }

}
```

## Change Permission

We have to give permission for our app to access internet.

```
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package = "com.example.myapplication">
    <uses-permission android:name ="android.permission.INTERNET"/>
    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:usesCleartextTraffic="true"
        android:theme="@style/Theme.MyApplication">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>

            <meta-data
                android:name="android.app.lib_name"
                android:value="" />
        </activity>
    </application>

</manifest>
```

## Sample Screenshot

<p align="center">
  <img src="https://user-images.githubusercontent.com/110366380/198543082-a34a3a15-40a7-4558-bd53-18cb4902c2d7.png">
</p>          

### Checking with Quora

<p align="center">
  <img src="https://user-images.githubusercontent.com/110366380/198543582-3943a9a6-e5c7-4374-9663-bf0a02de45ba.png">
</p>          

