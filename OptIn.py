# cocoa_keypress_monitor.py by Bjarte Johansen is licensed under a
# License: http://ljos.mit-license.org/
# https://gist.github.com/ljos/3019549

from AppKit import NSApplication, NSApp
from Foundation import NSObject, NSLog
from Cocoa import NSEvent, NSKeyDownMask
from PyObjCTools import AppHelper
import time
import sys


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        mask = NSKeyDownMask
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, handler)


def handler(event):
    sys.stdout.write(event.characters().description())
    sys.stdout.flush()

def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    try:
        AppHelper.runEventLoop()
    except KeyboardInterrupt as e:
        AppHelper.stopEventLoop()
        sys.exit(0)

if __name__ == '__main__':

    main()
