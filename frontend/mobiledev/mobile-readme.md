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


2. MainActivity.java
