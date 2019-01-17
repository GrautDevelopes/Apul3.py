#!/usr/bin/python
# -*- coding: utf-8 -*-
# Apul3.py Alpha v0.3 by GrautDevelopes
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium import webdriver
from colorama import init
from colorama import Fore, Back, Style
import itertools
import argparse
import random
import urllib
import errno
import time
import sys
import re
import os

init() # Init Colorama

# Source: https://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
# Source: https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
def writable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):  # If it's not already a directory.
        try:
            os.makedirs(prospective_dir)  # Make it.
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                saveline("[Apul3] Error: " + prospective_dir +
                         " is not a valid path and or could not be created.")
                raise argparse.ArgumentTypeError(
                    "[Apul3] Error: " + prospective_dir + " is not a valid path and or could not be created.")  # Incorrectly typed or couldn't be created.
    if os.access(prospective_dir, os.W_OK):  # If you can write to it.
        return prospective_dir  # It's good.
    else:
        saveline("[Apul3] Error: " + prospective_dir +
                 " is not a writable directory.")
        raise argparse.ArgumentTypeError(
            "[Apul3] Error: " + prospective_dir + " is not a writable directory.")  # Not enough permissions.


useragentaliases = {
    # Using "Random" will give you a random useragent
    
    # Chrome 67 on Windows 8.1
    "WindowsChrome": 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',

    # Internet Explorer 10 on Windows 8 
    "WindowsIE": 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',

    # Edge 38 on Windows 10
    "WindowsEdge": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',

    # Firefox 40.1 on Windows 7
    "WindowsFirefox": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',

    # Safari 7 on Mac OS X (Mavericks)
    "MacSafari": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',

    # Safari 7 on Apple iPhone iOS 11.4.1
    "iPhoneSafari": 'Mozilla/5.0 (iPhone; U; en; CPU iPhone OS 11_4_1 like Mac OS X; en) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/7.0.3 Mobile/8C148a Safari/6533.18.5',

    # Safari 7 on Apple iPad iOS 11.4.1
    "iPadSafari": 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/7.0.3 Mobile/10A5355d Safari/8536.25',
}

# Source: https://www.paddingleft.com/2017/03/20/python-cmd-argument-parsing-argparse/
# Source: https://docs.python.org/2/howto/argparse.html
# Source: http://www.pythonforbeginners.com/argparse/argparse-tutorial
# Source: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
parser = argparse.ArgumentParser(description="Automatic PopUp Logger")
parser.add_argument("redirectorlist",
                    help="List of redirectors in url (Ex: http://redirector.com/) format. Ex: redirectors.txt",
                    default="redirectors.txt")
parser.add_argument(
    "loads", type=int, help="Number of times to load a redirector. Ex: 1", default="1")
parser.add_argument("useragent",
                    help="The User-Agent or alias to appear as. What popups you want to get. Ex: WindowsChrome Ex: \"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36\"",
                    default="Chrome")
parser.add_argument(
    "-o", "--output", help="File to log the sites we found. Ex: sites.txt", default="sites.txt")
parser.add_argument("-ss", "--screenshot", type=writable_dir,
                    help="Take screenshots of all sites and save to this folder. Ex: /screens", default="/screens")
parser.add_argument("-ws", "--windowsize",
                    help="The size of the window to emulate and of screenshots. Helps to emulate mobile devices. Ex: 1024x768",
                    default="1024x768")
parser.add_argument("-to", "--timeout", help="The time to wait for a page to load before quitting in seconds. Ex: 15",
                    default="15")
parser.add_argument("-w", "--waitonpage", type=int,
                    help="The time to wait on page in seconds. Helps popup detection. Ex: 1", default="1")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="Log verbosely, logs which redirector gave which popup.")
parser.add_argument("-dvrd", '--disableverboseremoveduplicates', dest='disableverboseremoveduplicates',
                    action='store_true', help="Use to remove duplicate popups regardless of redirector.")
parser.add_argument("-footerleecher", "--footerleecher", action="store_true",
                    help="Attempt to get extra popups when there is a recognized original source link on the page.")
parser.add_argument("-uaa", "--useragentaliaslist", action="store_true",
                    help="The list of User-Agent aliases to appear as. Kind of popups you want to get.")



args = parser.parse_args()

if args.useragentaliaslist:
    for key, value in useragentaliases.items():
        print "Use " + key + " as useragent to appear as " + value
    print "Use Random as useragent to appear as any of the above."
    exit()

# Source: https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-whilst-preserving-order
# Source: http://www.peterbe.com/plog/uniqifiers-benchmark
sites = []
log = []


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


# Source: http://github.com/GrautDevelopes/Apul.py/
# Source: https://stackoverflow.com/questions/2104305/finding-elements-not-in-a-list
def saveprint():
    if args.verbose:
        if not args.disableverboseremoveduplicates:
            sitesuniq = []
            for site in sites:
                if re.sub(r"(\|.*)(\| hxx.*)", "\1", site) not in sitesuniq:
                    sitesuniq.append(site)
# List1:                 List2:                      List3:
# Example1 | ABC         Example1 | ABC | X          Example1 | ABC | X
# Example1 | ABC         Example1 | ABC | Y          Example2 | GHI | Z
# Example2 | GHI         Example2 | GHI | Z
    else:
        sitesuniq = f7(sites)  # Remove duplicate messages.
    if args.output:  # If saving
        logstream = open(args.output, 'a+')  # Open the log stream.
    for message in sitesuniq:  # For every message excluding the duplicates
        if message not in log:  # If it's not already in this session's log
            if '[Apul3] Error: ' in message:
                print Fore.RED + message + Style.RESET_ALL
            elif '[Apul3] Popup: ' in message:
                print Fore.GREEN + message + Style.RESET_ALL
            elif '[Apul3] Start of Redirector: ' in message:
                print Fore.YELLOW + message + Style.RESET_ALL
            elif '[Apul3] End of Redirector: ' in message:
                print Fore.BLUE + message + Style.RESET_ALL
            elif '[Apul3] Ended ' in message:
                print Fore.RED + message + Style.RESET_ALL
            elif '[Apul3] Starting ' in message:
                print Fore.GREEN + message + Style.RESET_ALL
            else: 
                print message  # Print the site.
            if args.output:  # If saving
                logstream.write('%s\n' % message)  # Put in the file.
            log.append(message)  # Add the site to this session's log.
#        else:  # If it is in this session's log.
#            print "[Apul3] Duplicate removed." # Just print the message. This is where the multiplying code is.


def saveprintline(line):
    if '[Apul3] Error: ' in line:
        print Fore.RED + line.strip() + Style.RESET_ALL
    elif '[Apul3] Popup: ' in line:
        print Fore.GREEN + line.strip() + Style.RESET_ALL
    elif '[Apul3] Start of Redirector: ' in line:
        print Fore.YELLOW + line.strip() + Style.RESET_ALL
    elif '[Apul3] End of Redirector: ' in line:
        print Fore.BLUE + line.strip() + Style.RESET_ALL
    elif '[Apul3] Ended ' in line:
        print Fore.RED + line.strip() + Style.RESET_ALL
    elif '[Apul3] Starting ' in line:
        print Fore.GREEN + line.strip() + Style.RESET_ALL
    else: 
        print line.strip()  # Print the site.
    logstream = open(args.output, 'a+')  # Open the log stream.
    logstream.write('%s\n' % line.strip())  # Write the line to the file.
    log.append(line.strip())  # Add to this session's log.


def saveline(line):
    logstream = open(args.output, 'a+')  # Open the log stream.
    logstream.write('%s\n' % line.strip())  # Write the line to the file.
    log.append(line.strip())  # Add to this session's log.


try:
    saveprintline("[Apul3] Starting " + str(time.time()) +
                  " Redirector list: " + args.redirectorlist)
    saveprintline("[Apul3] Command line: " + ' '.join(sys.argv))
    # Source: https://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python
    # Source: https://gist.github.com/ozen/e24c4d40b53a774d9b36
    useragent = args.useragent
    if useragent in useragentaliases:  # If the useragent is an alias
        # Look it up and assign it.
        useragent = useragentaliases[args.useragent]
    else:
        if 'Random' == useragent:  # If we need a random useragent
            useragent = useragentaliases[
                random.choice(useragentaliases.keys())]  # Get random useragent from aliases and set it.
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # Set User-Agent
    dcap["phantomjs.page.settings.userAgent"] = useragent
    dcap['phantomjs.page.customHeaders.User-Agent'] = useragent
    try:
        driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true','--ssl-protocol=any'], desired_capabilities=dcap)
        driver.capabilities["acceptSslCerts"] = True
    except WebDriverException as exception:
        saveline("[Apul3] Error: Could not start PhantomJS. {}".format(exception))
        raise WebDriverException(
            "[Apul3] Error: Could not start PhantomJS. {}".format(exception))
    saveprintline("[Apul3] Useragent: " + useragent)
    windowsizearray = args.windowsize.split('x')

    try:
        # Size output of screenshots
        driver.set_window_size(windowsizearray[0], windowsizearray[1])
    except WebDriverException as exception:
        saveline("[Apul3] Error: Could not set window size. {}".format(exception))
        raise WebDriverException(
            "[Apul3] Error: Could not set window size. {}".format(exception))
    try:
        driver.set_page_load_timeout(args.timeout)
        driver.set_script_timeout(args.waitonpage)
    except WebDriverException as exception:
        saveline("[Apul3] Error: Could not set load timeout. {}".format(exception))
        raise WebDriverException(
            "[Apul3] Error: Could not set load timeout. {}".format(exception))

    # Source: https://stackoverflow.com/questions/8009882/how-to-a-read-large-file-line-by-line-in-python
    # Source: https://stackoverflow.com/questions/2970780/pythonic-way-to-do-something-n-times-without-an-index-variable
    # Source: http://github.com/GrautDevelopes/Apul.py/
    popupcounttotal = 0  # Init the stats
    pagecounttotal = 0  # Init the stats
    popupcounttotaluniq = 0  # Init the stats
    pagecounttotaluniq = 0  # Init the stats

    with open(args.redirectorlist) as redirectorliststream:  # Open list of redirectors
        for line in redirectorliststream:  # For every redirector
            popupcount = 0  # Reset stats
            pagecount = 0  # Reset stats
            popupcountuniq = 0  # Reset stats
            pagecountuniq = 0  # Reset stats
            saveprintline("[Apul3] Start of Redirector: " + re.sub('htt', 'hxx',
                                                                   line.strip()))  # Print and log the beginning message with censored redirector.
            for i in range(args.loads):  # Repeat the list i times
                try:
                    # Tell the driver to load the redirector.
                    driver.get(line.strip())
                    breaker = False
                except Exception as exception:  # Was TimeoutException
                    saveprintline("[Apul3] Error: " + re.sub('htt', 'hxx',
                                                             line.strip()) + " could not be navigated to. Check network or timeout setting. {}".format(
                        exception))
                    breaker = True
                    break
                if breaker:
                    break
                # Wait a bit to redirect and for items to load.
                driver.implicitly_wait(args.waitonpage)
                # (Enhancements for a certain type of popup.) If common popup
                if "&r=&z=" in driver.current_url:
                    driver.implicitly_wait(2)
                if ".php?eps=" or ".php?q1=" in driver.current_url:
                    # Source: https://stackoverflow.com/questions/26566799/how-to-wait-until-the-page-is-loaded-with-selenium-for-python
                    try:
                        saveprintline("[Apul3] Common enhancement for " +
                                      re.sub('htt', 'hxx', driver.current_url) + " enabled.")
                        driver.implicitly_wait(args.waitonpage)
                        element = WebDriverWait(driver, float(args.waitonpage)).until(
                            EC.presence_of_element_located((By.ID, "FormattedNumber1")))
                    except TimeoutException as exception:
                        saveprintline(
                            "[Apul3] Error: Common enhancement for " +
                            re.sub('htt', 'hxx', driver.current_url) + " timed out. {}".format(exception))
                if "?a=AZ" and "pagex=0" and "s1=" in driver.current_url:
                    # Source: https://stackoverflow.com/questions/26566799/how-to-wait-until-the-page-is-loaded-with-selenium-for-python
                    try:
                        saveprintline("[Apul3] Common popup page enhancement for " +
                                      re.sub('htt', 'hxx', driver.current_url) + " enabled.")
                        driver.implicitly_wait(args.waitonpage)
                        element = WebDriverWait(driver, float(args.waitonpage)).until(
                            EC.presence_of_element_located((By.ID, "FormattedNumber1")))
                    except TimeoutException as exception:
                        saveprintline(
                            "[Apul3] Error: Common popup page enhancement for " +
                            re.sub('htt', 'hxx', driver.current_url) + " timed out. {}".format(exception))
                num = re.search(
                    r"((((((\(\d{3})|(\s\d{3}))((\)|-)|(\s|\) )|(\)-)?))?)|(\d{3}(-|\s)))?\d{3}(-|\s)\d{4})",
                    driver.current_url + driver.page_source)  # Search the URL and source code of the site for a number. A lot of false positives. Regex by Eclipse for Graut and the scambaiting community. https://0-eclipse-0.github.io/phone_regex.txt
                if num and len(num.group(0)) > 9:  # If we find a number
                    if args.verbose:
                        outline = "[Apul3] Popup: " + re.sub('htt', 'hxx', driver.current_url) + ' | {}'.format(
                            num.group(0)) + " | " + re.sub('htt', 'hxx',
                                                           line.strip())  # Print and log it as a popup while censoring the popup and redirector urls.
                    else:
                        outline = "[Apul3] Popup: " + re.sub('htt', 'hxx', driver.current_url) + ' | {}'.format(
                            num.group(0))  # Print and log it as a popup while censoring popup url.
                    # Count it as popup for redirector stats.
                    popupcount = popupcount + 1
                    # Count it as popup for total stats.
                    popupcounttotal = popupcounttotal + 1
                    if outline not in sites:
                        # Count it as popup for redirector stats.
                        popupcountuniq = popupcountuniq + 1
                        # Count it as popup for total stats.
                        popupcounttotaluniq = popupcounttotaluniq + 1
        
                else:  # If we don't find a number.
                    if args.verbose:
                        outline = "[Apul3] Page: " + re.sub('htt', 'hxx', driver.current_url) + " | " + re.sub('htt',
                                                                                                               'hxx',
                                                                                                               line.strip())  # Print and log it as a page while still censoring the urls just in case.
                    else:
                        outline = "[Apul3] Page: " + re.sub('htt', 'hxx',
                                                            driver.current_url)  # Print and log it as a page while still censoring the popup url.
                    if args.screenshot:  # If we need to take a screenshot
                        if not os.path.isfile(os.path.join(args.screenshot, urllib.quote_plus(
                                driver.current_url) + ".png")):  # and if we don't already have one
                            try:
                                driver.get_screenshot_as_file(os.path.join(args.screenshot, urllib.quote_plus(
                                    driver.current_url) + ".png"))  # Save the screenshot to disk, file name is the site's url encoded (percents).
                            except Exception as exception:
                                saveprintline("[Apul3] Error: " + re.sub('htt', 'hxx',
                                                                         line.strip()) + " screenshot of page could not be created. {}".format(
                                    exception))
                    # Count it as page for redirector stats.
                    pagecount = pagecount + 1
                    # Count it as page for total stats.
                    pagecounttotal = pagecounttotal + 1
                    if outline not in sites:
                        # Count it as page for redirector stats.
                        pagecountuniq = pagecount + 1
                        # Count it as page for total stats.
                        pagecounttotaluniq = pagecounttotal + 1
        
                if not breaker:
                    if args.screenshot:  # If we need to take a screenshot
                        if not os.path.isfile(os.path.join(args.screenshot, urllib.quote_plus(
                                driver.current_url) + ".png")):  # and if we don't already have one
                            try:
                                driver.get_screenshot_as_file(os.path.join(args.screenshot, urllib.quote_plus(
                                    driver.current_url) + ".png"))  # Save the screenshot to disk, file name is the site's url encoded (percents).
                            except Exception as exception:
                                saveprintline("[Apul3] Error: " + re.sub('htt', 'hxx',
                                                                         line.strip()) + " screenshot could not be created. {}".format(
                                    exception))
        
                # Add the message we constructed earlier to the list of sites
                sites.append(outline)
                saveprint()  # Save it to the log if we need to, then print it.
            saveprintline(
                "[Apul3] End of Redirector: " + re.sub('htt', 'hxx',
                                                       line.strip()) + " Popups found on redirector: " + str(
                    popupcount) + "/" + str(pagecount + popupcount) + " Unique Popups found on redirector: " + str(
                    popupcountuniq) + "/" + str(
                    pagecountuniq + popupcountuniq))  # Save and print the ending message with censored redirector and stats.
    driver.quit()  # Tell the driver to quit.
    saveprintline("[Apul3] Ended " + str(time.time()) + " End of Redirector list: " + args.redirectorlist + " Popups found: " + str(popupcounttotal) + "/" + str(pagecounttotal + popupcounttotal)) + " Unique Popups found: " + str(popupcounttotaluniq) + "/" + str(pagecounttotaluniq + popupcounttotaluniq)  # Save and print the final message with stats.
except KeyboardInterrupt, SystemExit:
    if line:
        driver.quit()  # Tell the driver to quit.
        saveprintline("[Apul3] Ended " + str(time.time()) + " Interrupted Redirector list: " + args.redirectorlist + " on " + re.sub('htt', 'hxx', line.strip()) + " Popups found: " + str(popupcounttotal) + "/" + str(pagecounttotal + popupcounttotal)) + " Unique Popups found: " + str(popupcounttotaluniq) + "/" + str(pagecounttotaluniq + popupcounttotaluniq)  # Save and print the final message with stats.
    else:
        driver.quit()
        saveprintline("[Apul3] Ended " + str(time.time()) + " Interrupted Redirector list: " + args.redirectorlist + " Popups found: " + str(popupcounttotal) + "/" + str(pagecounttotal + popupcounttotal)) + " Unique Popups found: " + str(popupcounttotaluniq) + "/" + str(pagecounttotaluniq + popupcounttotaluniq)  # Save and print the final message with stats.
# finally:
#  # Your code which is always executed.