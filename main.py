import json
from appium import webdriver
from selenium.webdriver.common.by import By

## Target App = Mx takatak

def main():
    desired_capabilities = {
        "appium:deviceName": "realme 3 Pro",
        "appium:udid": "f97e26c2",
        "platformName": "Android",
        "appium:platformVersion": "11",
        "appium:autoGrantPermissions": True,
        "unicodeKeyboard": False,
    }

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_capabilities)

    keyword_list = ['saami saami','dholida', 'oo antava','srivalli', 'sare bolo bewafa', 'maar khayegaa', 'meri jaan']

    output = launch(driver, keyword_list)

    with open('video-data.json', 'w') as outfile:
        json.dump(output, outfile)


##xapths 
videotab_xpath = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.HorizontalScrollView/android.widget.FrameLayout/android.widget.LinearLayout[2]/android.widget.TextView[2]"

copy_url_btn = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView[1]/android.view.ViewGroup[4]"

copy_audio_library_url = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]"

first_video_result = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.ImageView[1]"

def get_video_metaData(driver,keyword):
    temp_list = []
    count = 1
    while(count <= 20): 
        #pause screen by a tap
        driver.tap([(405,100),(675,1200)])
        driver.implicitly_wait(1000)
        #get meta data
        likes = driver.find_element(By.ID,"com.next.innovation.takatak:id/detail_like_count").text
        comments = driver.find_element(By.ID,"com.next.innovation.takatak:id/detail_comment_count").text
        #sound = driver.find_element(By.ID,"com.next.innovation.takatak:id/music_desc").text
        user = driver.find_element(By.ID,"com.next.innovation.takatak:id/tv_publisher_name").text
        desc = driver.find_element(By.ID,"com.next.innovation.takatak:id/detail_desc").text
        share = driver.find_element(By.ID,"com.next.innovation.takatak:id/detail_share_count").text
        #click share button
        driver.find_element(By.ID,"com.next.innovation.takatak:id/detail_share").click()
        #click copy url
        driver.find_element(By.XPATH,copy_url_btn).click()
        driver.get_clipboard()
        #get the copied url from android clipboard
        url = driver.get_clipboard_text()
        driver.implicitly_wait(1000)

        #create a dictionary of meta data and append to temporary list
        obj = {"url":url,"user" : user,"desc":desc,"likes":likes,"shares":share,"comments":comments}
        print(count,obj)
        temp_list.append(obj)
        count+=1
        driver.implicitly_wait(1000)
        driver.swipe(547,1034,530,567)
        driver.implicitly_wait(300)
        #tap to pause
        driver.tap([(405,100),(675,1200)])
    driver.tap([(405,100),(675,1200)])
    #create a key value pair of current keyword and array of videos metadata
    json = {keyword : temp_list}
    return json

def search_element(driver,keyword,output):
    #get cursor on searchbox and enter keyword to search
    driver.find_element(By.ID,"com.next.innovation.takatak:id/edit_input").click()
    driver.find_element(By.ID,"com.next.innovation.takatak:id/edit_input").send_keys(keyword)
    #hit search
    driver.execute_script("mobile:performEditorAction",{'action':'search'})
    #navigate to videos tab
    driver.find_element(By.XPATH,videotab_xpath).click()
    #click on the first video
    driver.find_element(By.XPATH,first_video_result).click()
    #call this function to get metaData for top 20 videos
    data = get_video_metaData(driver,keyword)
    output.append(data)
    driver.back()
    driver.find_element(By.ID,"com.next.innovation.takatak:id/iv_clear").click()

def launch(driver,keywordlist):
    OUTPUT = []
    ## The app icon is found using XPATH
    driver.find_element(By.XPATH,'//android.widget.TextView[@content-desc="MX TakaTak"]').click()
    driver.implicitly_wait(2000)
    ## click on bottom nav on search icon 
    driver.find_element(By.ID,"com.next.innovation.takatak:id/navDiscover").click()
    ## click on searchobx
    driver.find_element(By.ID,"com.next.innovation.takatak:id/tv_search").click()
    driver.implicitly_wait(2000)
    #call search_element for each keyword
    for keyword in keywordlist:
        search_element(driver,keyword,OUTPUT)
    return OUTPUT

if __name__ == '__main__':
    main()