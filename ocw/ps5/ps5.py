# 6.0001/6.00 Problem Set 5 - RSS Feed Filter

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import Tk, TOP, BOTTOM, RIGHT, END, Text, Button, Frame, \
                      Label, StringVar, Scrollbar, Y
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
            #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
            #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

# ======================
# Data structure design
# ======================

# Problem 1


class NewsStory:
    """
    Represents a single news story from a RSS feed.
    """

    def __init__(self, guid, title, description, link, pubdate):
        """
        :param guid: The news story's Globally Unique Identifier.
        :type guid: str
        :param title: The news story's title.
        :type title: str
        :param description: The news story's description.
        :type description: str
        :param link: The news story's link.
        :type link: str
        :param pubdate: The news story's publication date.
        :type pubdate: str
        """
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        """
        :returns: The Globally Unique Identifier of the NewsStory object.
        :rtype: str
        """
        return self.guid

    def get_title(self):
        """
        :returns: The title of the NewsStory object.
        :rtype: str
        """
        return self.title

    def get_description(self):
        """
        :returns: The description of the NewsStory object.
        :rtype: str
        """
        return self.description

    def get_link(self):
        """
        :returns: The link of the NewsStory object.
        :rtype: str
        """
        return self.link

    def get_pubdate(self):
        """
        :returns: The publication date of the NewsStory object.
        :rtype: str
        """
        return self.pubdate


# ======================
# Triggers
# ======================


class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS


# Problem 2
class PhraseTrigger(Trigger):
    """
    Represents a trigger for a phrase.
    """
    def __init__(self, phrase):
        """
        :param phrase: The phrase for the trigger; words should only be
                       separated by a space.
        :type phrase: str
        """
        self.phrase = phrase

    def is_phrase_in(self, text):
        """
        Checks if the phrase, separated only by spaces or punctuation, is in
        the provided text.

        :param phrase: The text to find the phrase in.
        :type phrase: str
        :returns: Whether or not the phrase in the text.
        :rtype: bool
        """
        phrase = self.phrase.lower()
        phrase_words = phrase.split(' ')

        # strip punctuation from text
        text = [' ' if c in string.punctuation else c for c in text.lower()]
        text_words = [word for word in ''.join(text).split(' ') if len(word)]

        if len(phrase_words) == 1:
            return phrase in text_words

        # handle phrases with multiple words
        try:
            first_word_index = text_words.index(phrase_words[0])
            phrase_word_count = 1
            index = first_word_index + phrase_word_count
            status = False

            # check if other words in phrase immediately follow first word
            while index < len(text_words):
                if phrase_words[phrase_word_count] == text_words[index]:
                    phrase_word_count += 1
                else:  # word after word in phrase is not part of the phrase
                    break
                if phrase_word_count == len(phrase_words):  # all words found
                    status = True
                    break
                index += 1
            return status
        except ValueError:  # first word of phrase is not in the text
            return False


# Problem 3
class TitleTrigger(PhraseTrigger):
    """
    Represents a trigger for a phrase in a news story's title.
    """
    def __init__(self, phrase):
        """
        :param phrase: The phrase for the trigger; words should only be
                       separated by a space.
        :type phrase: str
        """
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        """
        Checks if the phrase is in the provided news story's title.

        :param story: The story to check the publication date for.
        :type story: NewsStory
        :returns: Whether or not the phrase in the news story's title.
        :rtype: bool
        """
        title = story.get_title()
        return self.is_phrase_in(title)


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    """
    Represents a trigger for a phrase in a news story's description.
    """
    def __init__(self, phrase):
        """
        :param phrase: The phrase for the trigger; words should only be
                       separated by a space.
        :type phrase: str
        """
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        """
        Checks if the phrase is in the provided news story's description.

        :param story: The story to check the publication date for.
        :type story: NewsStory
        :returns: Whether or not the phrase in the news story's description.
        :rtype: bool
        """
        description = story.get_description()
        return self.is_phrase_in(description)

# TIME TRIGGERS


# Problem 5
class TimeTrigger(Trigger):
    """
    Represents a trigger for a certain time.
    """
    def __init__(self, time):
        """
        :param time: The time for the trigger following the format of
                     "%d %b %Y %H:%M:%S" in the EST time zone.
        :type time: str
        """
        self.time = datetime.strptime(time, '%d %b %Y %H:%M:%S') \
                            .replace(tzinfo=pytz.timezone('EST'))


# Problem 6
class BeforeTrigger(TimeTrigger):
    """
    Represents a trigger for a news story published before a certain time.
    """
    def __init__(self, time):
        """
        :param time: The time for the trigger following the format of
                     "%d %b %Y %H:%M:%S" in the EST time zone.
        :type time: str
        """
        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        """
        Checks if the provided news story is published before the trigger's
        time.

        :param story: The story to check the publication date for.
        :type story: NewsStory
        :returns: Whether or not the story was published before the trigger's
                  time.
        :rtype: bool
        """
        before_date = story.get_pubdate().replace(tzinfo=pytz.timezone('EST'))
        return before_date < self.time


class AfterTrigger(TimeTrigger):
    """
    Represents a trigger for a news story published after a certain time.
    """
    def __init__(self, time):
        """
        :param time: The time for the trigger following the format of
                     "%d %b %Y %H:%M:%S" in the EST time zone.
        :type time: str
        """
        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        """
        Checks if the provided news story is published after the trigger's
        time.

        :param story: The story to check the publication date for.
        :type story: NewsStory
        :returns: Whether or not the story was published after the trigger's
                  time.
        :rtype: bool
        """
        after_date = story.get_pubdate().replace(tzinfo=pytz.timezone('EST'))
        return after_date > self.time

# COMPOSITE TRIGGERS


# Problem 7
class NotTrigger(Trigger):
    """
    Represents a trigger that inverts the evaluation of the given trigger for a
    specific story, used to exclude stories that satisfy the given trigger.
    """
    def __init__(self, trigger):
        """
        :param trigger: The trigger to invert the evaluation for.
        :type trigger: Trigger
        """
        self.trigger = trigger

    def evaluate(self, story):
        """
        :param story: The news story to check.
        :type story: NewsStory
        """
        return not self.trigger.evaluate(story)


# Problem 8
class AndTrigger(Trigger):
    """
    Represents a trigger that checks if a specific story satisfies both given
    triggers.
    """
    def __init__(self, trigger1, trigger2):
        """
        :param trigger1: The first trigger to check.
        :type trigger1: Trigger
        :param trigger2: The second trigger to check.
        :type trigger2: Trigger
        """
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        """
        :param story: The news story to check.
        :type story: NewsStory
        :returns: Whether or not a specific story satisfies both triggers.
        :rtype: bool
        """
        response1 = self.trigger1.evaluate(story)
        response2 = self.trigger2.evaluate(story)
        return response1 and response2


# Problem 9
class OrTrigger(Trigger):
    """
    Represents a trigger that checks if a specific story satisfies at least one
    of the given triggers.
    """
    def __init__(self, trigger1, trigger2):
        """
        :param trigger1: The first trigger to check.
        :type trigger1: Trigger
        :param trigger2: The second trigger to check.
        :type trigger2: Trigger
        """
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        """
        :param story: The news story to check.
        :type story: NewsStory
        :returns: Whether or not a specific story satisfies one of the
        triggers.
        :rtype: bool
        """
        response1 = self.trigger1.evaluate(story)
        response2 = self.trigger2.evaluate(story)
        return response1 or response2


# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist
             fires.
    """
    return [s for s in stories if any(t.evaluate(s) for t in triggerlist)]


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    trigger_file = open(filename, 'r')
    triggers = {}
    response = []
    for line in trigger_file:
        line = line.rstrip()
        # ignore comments and whitespace
        if len(line) == 0 or line.startswith('//'):
            continue
        args = line.split(',')
        [trigger_name, trigger_type] = args[:2]
        # make trigger objects and populate dict accordingly
        if trigger_name == 'ADD':  # finish making triggers
            response = [triggers.get(n) for n in args[1:] if triggers.get(n)]
            break
        if trigger_type == 'TITLE':
            triggers[trigger_name] = TitleTrigger(args[2])
        if trigger_type == 'DESCRIPTION':
            triggers[trigger_name] = DescriptionTrigger(args[2])
        if trigger_type == 'AFTER':
            triggers[trigger_name] = AfterTrigger(args[2])
        if trigger_type == 'BEFORE':
            triggers[trigger_name] = BeforeTrigger(args[2])
        if trigger_type == 'NOT':
            obj = triggers.get(args[2], None)
            if obj is None:  # ignore invalid triggers
                continue
            triggers[trigger_name] = NotTrigger(obj)
        if trigger_type == 'AND':
            obj1 = triggers.get(args[2], None)
            obj2 = triggers.get(args[3], None)
            if obj1 is None or obj2 is None:  # ignore invalid triggers
                continue
            triggers[trigger_name] = AndTrigger(obj1, obj2)
        if trigger_type == 'OR':
            obj1 = triggers.get(args[2], None)
            obj2 = triggers.get(args[3], None)
            if obj1 is None or obj2 is None:  # ignore invalid triggers
                continue
            triggers[trigger_name] = OrTrigger(obj1, obj2)
    return response


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to
    # to correspond what is currently in the news
    try:
        """
        t1 = TitleTrigger("Trump")
        t2 = DescriptionTrigger("American people")
        t3 = DescriptionTrigger("research")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]
        """

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master,
                    font=("Helvetica", 14),
                    yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n{}\n".format('-' * 63), "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n{}\n".format('*' * 69), "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
