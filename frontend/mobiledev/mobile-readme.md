# Steps for Mobile App Setup

For the first iteration of our project, we will be implementing a `web view` on the mobile app for our web app.

In order to have a similar browsing experience on the mobile, we have to make sure we design our website with these recommendation:

1. Make website mobile-friendly by using bootstrap and using a mobile first approach.
2. Take in consideration, the width and height constraints - The mobile devices are smaller in width and height. The pages need to shrink and not stretch beyond the natural width of the phone. We can scroll Vertically but horizontal scrolling is very difficult for mobile users.
3. We should have no `island page` on our website. There should be link available on all pages to navigate to related pages.
4. We can make use of `back` button, but the user experience won't be good.
5. If we are linking to external domains, we must have `_blank` as our link target. This is to prevent external sites opening within our app.

## Technical Specification

To make the web app view, we have choosen to do it using `Java` in `Android Studio`. The `Android Studio` is very resource intensive but the emulator features are well suited for testing purpose for our app.

### Creating a new project for the `mobile app`
- Select a new project.
- Select `Empty Activity` template.
- Name the application, Preferably same as the `web app`
- Select the language as `Java`.
- Choose the required `Android Version`. The default `SDK` will work in this scenario.

#### Sample Screenshot

<p align="center">
  <img src="https://user-images.githubusercontent.com/110366380/198543082-a34a3a15-40a7-4558-bd53-18cb4902c2d7.png">
</p>          

**Note**: The project might take a while to load, The `gradle` build takes a long time. We can move the gradle as a background process. That would save us some loading time.

### File Structure

Once the project is open, we will have 2 main files. One for the design with `.xml` extension and another one with `.java` extension for our logic.

1. `activity_main.xml` - This file contains all the design layout for the applicatoin.

- It already has prepopulated code for a constraint layout, but we will be using a `RelativeLayout` for the web view.
- We need the full screen for the layout, so we define the width & height to `match_parent`. 
- We will also need the Web View to be full screen, so we change its layout to `match_parent`. It will take the full available space of the relative layout.

**Note**: Don't forget to give an `android:id` for the WebView, else we won't be able to access it while writing the Java code.

Our code for this file `activity_main.xml` will be:

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


### Checking with Quora

<p align="center">
  <img src="https://user-images.githubusercontent.com/110366380/198543582-3943a9a6-e5c7-4374-9663-bf0a02de45ba.png">
</p>          

