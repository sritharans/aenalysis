# Test - Build - Submit

## Test

1. This application uses the same rendering and JavaScript Engine as the Chrome Browser so development and testing can be done as a web app and in the browser.

2. To test the PWA application on a device, follow the getting started guide here: https://docs.microsoft.com/en-us/microsoft-edge/progressive-web-apps-edgehtml/get-started

> **Note:** Looking for some debugging tools that work on all your platforms? Try [Vorlon.js](http://www.vorlonjs.com/). It makes mobile testing a breeze, and works inside the app PWA Builder apps.

## Build

1. Download and install the [Java SDK](http://www.oracle.com/technetwork/java/javase/downloads/index.html).

2. [Download](http://developer.android.com/sdk/installing/index.html?pkg=studio) and install Android Studio and the Android SDK.

3. Open the Gradle file from Android Studio (import project)

4. (Optional) Customize the splash screen of the app. Edit `app\res\drawable\splash.xml` and specify the image preference. If found, the PWA Builder will place a suggested splash screen in `app\res\mipmap\ic_splash.png`.

4. Use the Build Menu to create package.


## Submit to Store

1. Set up a Android Developer account [here](https://play.google.com/apps/publish/signup/).

2. Reserve the name of your app.

3. Upload your apk package.