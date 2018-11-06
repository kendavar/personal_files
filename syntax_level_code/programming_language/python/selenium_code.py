# import selenium webdriver
  from selenium import webdriver

# open a chrome browser
  driver=webdriver.Chrome()

# open a url in the browser
  driver.get(url)

# find element by name and enter the text into it
  driver.find_element_by_name("f.search").send_keys("Economics")

# time sleep to make it work properly
  import time
  time.sleep(2)

# switch to a frame
  driver.switch_to_frame("frameName")

# switch to the first frame 
  driver.switch_to_default_content()
  #--switch_to_default_content() will return you to the top of the document. What was happening is you switched into the first   iframe, switched back to the top of the document, then tried to find the second iframe. Selenium can't find the second iframe, because it's inside of the first iframe.


# print all the function used in the driver
  print dir(driver)

# click the button using css selector and dot has to be added to the class at begining and remove space to add dots
  e.g<button class="btn btn-big-link btn-search">Search</button>
  !driver.find_element_by_css_selector("btn btn-big-link btn-search").click()
    driver.find_element_by_css_selector(".btn.btn-big-link.btn-search").click()

#set window height and width
  driver.set_window_size(width, height)
  driver.set_window_size(1024, 1024)

#this is method to get the screenshot of a element in page
  element = driver.find_element_by_id('video')
  location = element.location
  print location#output:{'y': 32, 'x': 73.546875}
  size = element.size#size of element in web page
  print size#output:{'width': 1058, 'height': 594}
  driver.save_screenshot(filename)#used to take screenshot
  im = Image.open(filename)#open image
  left = location['x']
  print left#output:73.546875
  top = location['y']
  print top#output: 32
  right = location['x'] + size['width']
  print right#output:1131.546875
  bottom = location['y'] + size['height']
  print bottom#output:626
  "This round off is only required only if we get the 
    left=int(round(left))
    right=int(round(right))
  print left,right#output:74 1132
  im = im.crop((left, top, right, bottom))#used to crop the inner image element
  im.save(filename)#save the image(it overwrite if filename exits)

#used to make sure the alert pop up box doesn't cause a problem when web page is loaded
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException

try:
    WebDriverWait(self.driver, 3).until(EC.alert_is_present())
    alert = self.driver.switch_to_alert()
    alert.accept()
    print 'Alert was accepted'
except UnexpectedAlertPresentException:
    alert.send_keys('8080')
    alert.dismiss()
except:
    pass

#if their are more then one window we use this to be in correct window
   #--Returns the handles of all windows within the current session.
    driver.current_window_handle
   #--Returns the handle of the current window.
    driver.window_handles
   #ex.
    if len(self.webpage_text) < 1000 :
            current_window_handle =    self.driver.current_window_handle#get current window
            window_handles = self.driver.window_handles#get all the windows opened
            for window_handle in window_handles:
                self.driver.switch_to_window(window_handle)#switch to one by one to each window 
                self.get_webpage_text_in_current_frame([])#funtion in program**not imp
                if window_handle != current_window_handle:
                    self.driver.close()
            self.driver.switch_to_window(current_window_handle)
            self.driver.switch_to_default_content()
            current_url = self.driver.current_url
        return current_url, self.webpage_text

#IT Gets the URL of the current page.
    driver.current_url

#for mobile devices set selenium browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
mobile_emulation = {
     "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
     "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(chrome_options = chrome_options)
driver.get("http://rss.feedsportal.com/c/35508/f/677693/s/4ade980c/sc/19/l/0L0Smensfitness0N0Cnutrition0Cwhat0Eto0Edrink0Cfall0Ebooze0Ehas0Enothing0Edo0Epumpkin/story01.htm")


#tablet chrome
mobile_emulation = {"deviceMetrics": { "width":960,"height":600,"pixelRatio":2.0},"userAgent":"Mozilla/5.0 (Linux; Android 4.3; Nexus 7 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Safari/537.36"}
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(chrome_options = chrome_options)

#when it is difficult to get the tag use this
self.driver.execute_script("""try {
      (function() {
        function jqReady($) {
          var hookCtx = {
            siteGuid: 'aaf35e5f84a07252a9830cff120252a7',
            sitePlacementId: 5831,
            userGuid: '',
            impressionHash: 'a7655d30c17468d6b0868285f7ab613b',
            pageUrl: 'http:\/\/epxkb8zz4ssdv7b.global.ssl.fastly.net\/next\/d887011\/videoPlayer\/assets\/html\/iabDisplay.html',
            partnerDomain: function() { return 'epxkb8zz4ssdv7b.global.ssl.fastly.net'; },
            numberOfArticles: 8,
            isIframe: false,
            isJsonp: true,
            containerId: 'grv-personalization-159'
          };

          var event = {
      event: 'impressionServed',
      version: 1,
      numberOfArticles: hookCtx.numberOfArticles,
      hasUserGuid: hookCtx.userGuid != ''
    };

    if(hookCtx.isIframe) {
      console.log('Posting Grv event %o to Grv /wl frame to be proxied to Disqus', event);
      event.grvProxyPostMessageUp = window.location.protocol + '//disqus.com';
      window.parent.postMessage('json|' + JSON.stringify(event), hookCtx.pageUrl);
    }
    else if(hookCtx.isJsonp) {
      console.log('Posting Grv event %o to Disqus', event);
      window.parent.postMessage(JSON.stringify(event), window.location.protocol + '//disqus.com');
    }
        }

        if(window.$grv)
          jqReady($grv);
        else
          (window.grvJqueryLoadedCallbacks || (window.grvJqueryLoadedCallbacks = [])).push(jqReady);
      })();
    }
    catch(ex) {
      if(window.console && console.warn) {
        console.warn('Grv suppressing widget hook footer JS exception:');
        console.warn(ex);
      }
    }""")

#Lazy load
when the web content will only load when they are visible.or scrolled.
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
used to scroll bottom of the screen.

#wait
used to wait for the page to load the element
WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,"grv_widget")))
WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.className, "iframe")))


#how to switch between tabs
from selenium.webdriver.common.keys import Keys
#Set current_window_handle to main tab
main_tab = driver.current_window_handle

# Get all links
list_links = self.driver(By.XPATH, "//a/" )

#Iterate over links
for element in list_links:

  # Open link in new tab 
  link.send_keys(Keys.CONTROL + Keys.SHIFT + Keys.RETURN)

  # Switch focus to newly opened tab using driver.window_handles[1]
  # driver.window_handles[1] => [1] for new tab index.
  driver.switch_to_window(driver.window_handles[1])

  /*** Do something OR Grabbing content using XPATH ***/

  #Now close newly opened tab
  driver.close()

  #Again switch to main tab/ previous tab
  driver.switch_to_window(main_tab)
#actions
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(hidden_submenu)
actions.perform()


#desktop useragent
fp.set_preference("general.useragent.override","Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0")

#for firefox we have to set the profile for using mobile
fp = webdriver.FirefoxProfile()
fp.set_preference("general.useragent.override","Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19")
browser = webdriver.Firefox(firefox_profile=fp)
browser.set_window_size(360,640)

#for firefox we have to set the profile for using tablet
fp = webdriver.FirefoxProfile()
fp.set_preference("general.useragent.override","Mozilla/5.0 (Linux; Android 4.3; Nexus 7 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Safari/537.36")
browser = webdriver.Firefox(firefox_profile=fp)
browser.set_window_size(960,600)


#kill firefox browser
ps -ef | grep -v grep | grep "Xvfb" | awk '{print $2}' | xargs kill -9

#disbale plugins firefox
firefoxProfile = webdriver.FirefoxProfile()
## Disable CSS
firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
## Disable images
firefoxProfile.st_preference('permissions.default.image', 2)
## Disable Flash
firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
#disable pop of boxs
fp.set_preference("intl.accept_languages", "no,en-us,en")
#set response timeout
fp.set_preference("http.response.timeout", 120) 
#set script run time
fp.set_preference("dom.max_script_run_time", 120)
br = webdriver.Firefox(firefox_profile=fp)


#disable pugins chrome
op0 = Options()
op0.add_argument("--disable-plugins-discovery"   
  prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs) 
br0 = webdriver.Chrome(chrome_options=op0)

--firefox
fp = webdriver.FirefoxProfile()
fp.set_preference('permissions.default.stylesheet', 2)
fp.set_preference('permissions.default.image', 2)
fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

   



