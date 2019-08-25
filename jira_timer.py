import Xlib
import Xlib.display
import time
from selenium import webdriver
import sys
import subprocess


def getName():
    disp = Xlib.display.Display()
    window = disp.get_input_focus().focus
    return window.get_wm_class()[0]


def getDomain():
    return driver.current_url


def getBranch():
    branch = subprocess.run(["git", "-C", sys.argv[1], "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE)
    return branch.stdout.strip().decode("utf-8")


driver = webdriver.Chrome()
activities = []
name = getName()
past_time = round(time.time())

while True:
    current_name = getName()
    branch = getBranch()
    domain = ''
    changed = False

    if "code" in name:
        current_branch = getBranch()
        if current_branch != branch:
            changed = True

    if "chromium" in name:
        current_domain = getDomain()
        if current_domain != domain:
            changed = True
    
    if name != current_name or changed == True:
        cat_type = "other"
        if "code" in name:
            branch = getBranch()
            cat_type = "coding"

        if "chromium" in name:
            name = "chromium"
            domain = getDomain()
            cat_type = "browsing"
            if "udemy" in domain:
                sub_type = "course"
            elif "confluence" in domain or "jira" in domain or "bitbucket" in domain or "cgi" in domain:
                sub_type = "business"
            elif "draw" in domain:
                sub_type = "mockup"
            else:
                sub_type = "research"

        time_difference = round(time.time()) - past_time
        current_object = {
            "type": cat_type,
            "name": name,
            "time_difference": time_difference 
        }

        for activity in activities:
            if activity['type'] == cat_type:
                for subType in activity["subType"]:
                    
                    if cat_type == "coding":
                        if subType["branch"] == branch:
                            branch = ''
                            subType["time_spent"] += current_object["time_difference"]
                
                    if cat_type == "browsing":
                        if subType["type"] == sub_type:
                            sub_type = ''
                            subType["time_spent"] += current_object["time_difference"]
                            if domain not in subType["domains"]:
                                subType["domains"].append(domain)
                current_object = ''

        if current_object != '':
            if cat_type == "coding":
                activities.append(
                    {
                        "type": current_object['type'], 
                        "subType": [
                            {
                                "branch": branch, 
                                "time_spent": current_object['time_difference']
                            }
                        ]
                    }
                )
                
            if cat_type == "browsing":
                activities.append(
                    {
                        "type": current_object['type'], 
                        "subType": [
                            {
                                "type": sub_type,
                                "time_spent": current_object['time_difference'],
                                "domains": [domain]
                            }
                        ]
                    }
                )
            current_object = ''

        name = current_name
        past_time = round(time.time())
        print(activities)

    time.sleep(1)