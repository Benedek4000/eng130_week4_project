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

2. `MainActivity.java` - This file include all the code required to convert the web app to the mobile app. Some key things required:

- We need to link our `WebView` defined in `activity_main.xml` to this file.
- By default, `WebView` does not support `JavaScript` so we have to explicitly Enable it.
- The default behaviour of the back button is to take us out of the application. We need to overwrite this feature.

```
package com.example.testapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends AppCompatActivity {

    private WebView webView; // Local Variable for WebView

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // To prevent user to leave the app for links clicked
        CustomWebViewClient client = new CustomWebViewClient(this);
        webView = findViewById(R.id.webView); // Linking the id to the one in activity_main.xml
        // To make sure webView uses the client custom webView
        webView.setWebViewClient(client);
        webView.getSettings().setJavaScriptEnabled(true); // Enable JavaScript
        webView.loadUrl("https://www.quora.com"); // Domain name of web app to convert

    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event){
        // If back button is pressed, and its possible to go back
        if(keyCode == KeyEvent.KEYCODE_BACK && this.webView.canGoBack()){
            this.webView.goBack(); // Go back to previous page
            return true;
        }
        return super.onKeyDown(keyCode, event); // If we can't go back, we will exit the application
    }
}

// To prevent the user to leave the app and go to external browser.
class CustomWebViewClient extends WebViewClient {
    private Activity activity;

    // Constructor
    public CustomWebViewClient(Activity activity){
        this.activity = activity;
    }

    // For API  < 24 - These API uses url as string
    @Override
    public boolean shouldOverrideUrlLoading(WebView webView, String url){
        return false; // To load all the links inside the application, True will load in external browser
    }

    // For API >= 24 = These API uses WebResourceRequest for the url(request)
    @Override
    public boolean shouldOverrideUrlLoading(WebView webView, WebResourceRequest request){
        return false; // To load all the links inside the application, True will load in external browser
    }
}
```

### Change App Permission - To Allow Internet Access for the app.

- We have to give permission for our app to access internet - `<uses-permission android:name="android.permission.INTERNET" />`.
- To use cleartext network traffic, HTTP in our case - `android:usesCleartextTraffic="true"`

The `AndroidManifest.xml` file will be:

```
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:usesCleartextTraffic="true"
        android:theme="@style/Theme.TestApplication"
        tools:targetApi="31">
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

### Choosing Image Icon for the App

- Right Click on App, Choose New, Image Asset



### Checking with Quora

<p align="center">
  <img src="https://user-images.githubusercontent.com/110366380/198543582-3943a9a6-e5c7-4374-9663-bf0a02de45ba.png">
</p>          


## Setting up Our `Web App` as a `Mobile App`

- To create a web view in mobile for our web app, we first have to run the app.
- Once we have a running app, we can use the `ip address` of our localhost as the `source ip` for the `mobile app`.
- To run the app, in `Visual Studio Code` navigate to the `frontend` branch/folder.
- Run `app.py` by typing `python app.py` on the terminal.
- We need to have the following packages installed before running the above command.
  - `Flask` - Python micro framework for web development - `pip install flask`
  - `OpenCV` - Python package for real-time capture of videos - `pip install opencv-python`
  - `PyAudio` - Python bindings for PortAudiov19 [**PortAudio** is a free, cross-platform, open-source, audio I/O library] - `pip install PyAudio`
  - `MoviePy` - Python library for video editing - `pip install moviepy`
- After we successfully run the command, we can type the ip `127.0.0.1` on the browser's address bar and we get the current version of our web app.

<p align="center">
  <img src="https://user-images.githubusercontent.com/110366380/198684384-a176002f-3980-4292-a0df-d1d684c9fc5f.png">
</p>

### Converting the running web app to mobile app

- Now we can replace the above url to our localhost address.
```
 webView.loadUrl("http:10.0.2.2");
```
**Imp Note**: In Android, to access the local host we used `10.0.2.2`.

#### Sample screenshots of our `Mobile App`

<p align="center">
  <img src="https://user-images.githubusercontent.com/110366380/198686574-9dd085fb-67b6-4e40-a930-1676f08f0852.png">
  <img src="https://user-images.githubusercontent.com/110366380/198686868-1b47d4f7-d1c9-4f4c-a8fd-0d50bde3298a.png">
  <img src="https://user-images.githubusercontent.com/110366380/198686904-2659672b-bbde-4981-b21d-ba173486b687.png">
</p>

