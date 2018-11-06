//change application id 
"1.select app"
"2.Right click and select open module settings"
"3.go to favours and then application id"
(All application id should be unique and they are the file path to src)


//to change the textview path used this code on sectionpage
public void onBackPressed()
    {
        if(webview.canGoBack()){
            webview.goBack();
			WebBackForwardList mWebBackForwardList = webview.copyBackForwardList();
			String historyUrl = mWebBackForwardList.getItemAtIndex(mWebBackForwardList.getCurrentIndex()).getUrl();
			Log.i("onbackpress",historyUrl);
			change(historyUrl);
        }
        else{
            super.onBackPressed();
        }
    }

//to change the textview path when sublink is clicked on sectonpage
    webview.setWebViewClient(new WebViewClient() {
        	public void onPageStarted(WebView view, String url, Bitmap favicon) {
        		dialog.show();
        	  }
        	// load url
			public boolean shouldOverrideUrlLoading(WebView view, String url) {
        		Log.i("sublink", url);
				change(url);
        		view.loadUrl(url);
        	    return true;
        	}
 
        	// when finish loading page
			public void onPageFinished(WebView view, String url) {
        	    if(dialog.isShowing()) {
        	        dialog.dismiss();
        	}
        	}

        	});
//function does the change on sectionpage
 public void change(String url){
		String str2=url.replace("file:///android_asset/Files/","").trim();
		if(str2.length()!=9) {
			Log.i("substring", ""+str2.length());
			cur1 = db.rawQuery("select _id,sectionid,chapterid,link from bm_section where link = ?",
					new String[]{"" + str2});
			cur1.moveToFirst();
			Log.i("substring", str2 + " " + cur1.getString(cur1.getColumnIndex("chapterid")) + Html.fromHtml("&rarr;") + cur1.getString(cur1.getColumnIndex("sectionid")));
			path.setText(cur1.getString(cur1.getColumnIndex("chapterid")) + Html.fromHtml("&rarr;") + cur1.getString(cur1.getColumnIndex("sectionid")));
		}
		Log.i("substring", ""+str2.length());

	}

//verification of apk
"1.clean project"
 ->BUILD->clean project
"2.First generate a signed apk"
  ->Build->generate signed apk
  ->PATH /Downloads/kdownloads/vt.keystore
  key alias->key1
  All passwords are 2015vulcantech

"3.go to folder where apk is stored

"4.For verification run this commands"
$ jarsigner -verify -verbose -certs my_application.apk >application.log

"if any error occurs:-"{
  ERRORs LIKE 
  !This jar contains entries whose certificate chain is not validated
  !This jar contains signatures that does not include a timestamp. Without a timestamp, users may not be able to validate this jar after the signer certificate's expiration date (2040-07-21) or after any future revocation date

  "to find java version"
  $ sudo apt-get update
  $ java -version

  "To correct the errors we use jdk version 6,Their is no problem in the build but jarsigner only works with jdk 6"
  sudo apt-get install oracle-java6-installer

  "Then run step 3 again"
}
"In log we get message like this the verification was succesfull"
jar verified.


"5.Zipalign the apk file.Its used to compress the files"
$./zipalign -v 4 intput.apk output.apk >zipalign.log 
  "if zipalign gives error"
    !zipalign: command not found
   "Follow this steps"
    1.Open terminal (CTRL + t)(skip if opened terminal
    2.cd YOUR_PATH/android-sdk-linux/build-tools/XX.X.X(any api or sdk version while do)
    3.(sudo cp zipalign /usr/bin/) or copy the zipalign script to the folder where apk is stored.
    4.Open the folder where is located your apk in the terminal.(skip if manually copied)
    5.Execute ./zipalign -v 4 YOUR_APK.apk YOUR_APK.apk >zipalign.log

"in log if we get following message then zipalign is succesful"
Verification succesful


//we were to change the list view when it was clicked to read and unread.
   "create a column read and unread
   "we use get view to solve it
	adapter = new SimpleCursorAdapter(
				this,
				R.layout.itat,
				cur,
				new String[] {"meta_title","title", "time"},
				new int[] {R.id.metatitle,R.id.chapterid, R.id.title})
        {
            @Override
            public View getView(int position, View convertView, ViewGroup parent)//position in list
            {
                final View row = super.getView(position, convertView, parent);
                Cursor cursor = (Cursor) adapter.getItem(position);//gets adapters position
                if (cursor.getInt(cursor.getColumnIndex("read")) == 1)//compares the db read value is 1 or not
                    row.setBackgroundResource(android.R.color.holo_green_light);//if 1 change the row or item list color
                else//if need
                return row;//return the view to the adapter
            }
        };

//How to add icons in android studio
http://stackoverflow.com/questions/18094313/android-development-unable-to-create-an-icon-drawable-ic-action-search

In Android studio:

Right click the Drawable folder > Select New > Image Asset

(Alternatively, click shift, shift and type 'Image Asset")

In the dialog which popped up click 'OK'








 
