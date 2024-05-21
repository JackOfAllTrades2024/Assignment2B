
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  IFB104, "Building IT Systems", Semester 1, 2024.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#  Put your student number here as an integer and your name as a
#  character string:
#
student_number = 11774797
student_name   = 'Jacob Shevlin - Krell'
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assessment Task 2 Description----------------------------------#
#
#  In this assessment task you will combine your knowledge of Python
#  programming, HTML-style mark-up languages, pattern matching,
#  database management, and Graphical User Interface design to produce
#  a robust, interactive "app" that allows its user to view and save
#  data from multiple online sources.
#
#  See the client's briefings accompanying this file for full
#  details.
#
#  Note that this assessable assignment is in multiple parts,
#  simulating incremental release of instructions by a paying
#  "client".  This single template file will be used for all parts,
#  together with some non-Python support files.
#
#--------------------------------------------------------------------#



#-----Set up---------------------------------------------------------#
#
# This section imports standard Python 3 modules sufficient to
# complete this assignment.  Don't change any of the code in this
# section, but you are free to import other Python 3 modules
# to support your solution, provided they are standard ones that
# are already supplied by default as part of a normal Python/IDLE
# installation.
#
# However, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# A function for opening a web document given its URL.
# [You WILL need to use this function in your solution,
# either directly or via the "download" function below.]
from urllib.request import urlopen

# Some standard Tkinter functions.  [You WILL need to use
# SOME of these functions in your solution.]  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: Although you can import individual widgets
# from the "tkinter.tkk" module, DON'T import ALL of them
# using a "*" wildcard because the "tkinter.tkk" module
# includes alternative versions of standard widgets
# like "Label" which leads to confusion.  If you want to use
# a widget from the tkinter.ttk module name it explicitly,
# as is done below for the progress bar widget.)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined
# via a regular expression.  [You do not necessarily need to
# use these functions in your solution, because the problem
# may be solvable with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.]
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  [You WILL need to use this function
# in your solution.]
from webbrowser import open as urldisplay

# All the standard SQLite database functions.  [You WILL need
# to use some of these in your solution.]
from sqlite3 import *

#
#--------------------------------------------------------------------#



#-----Validity Check-------------------------------------------------#
#
# This section confirms that the student has declared their
# authorship.  You must NOT change any of the code below.
#

if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()

#
#--------------------------------------------------------------------#



#-----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  You are not required to use this function, but it may
# save you some effort.  Feel free to modify the function or copy
# parts of it into your own code.
#

# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.  However, the root cause of the
# problem is not always easy to diagnose, depending on the quality
# of the response returned by the web server, so the error
# messages generated by the function below are indicative only.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we discourage using this
#      option as it is both unreliable and unethical to
#      override the wishes of the web document provider!
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'downloaded_document',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             incognito = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception sometimes raised when a web server
    # denies access to a document
    from urllib.error import HTTPError

    # Import an exception raised when a web document cannot
    # be downloaded due to some communication error
    from urllib.error import URLError

    # Open the web document for reading (and make a "best
    # guess" about why if the attempt fails, which may or
    # may not be the correct explanation depending on how
    # well behaved the web server is!)
    try:
        if incognito:
            # Pretend to be a web browser instead of
            # a Python script (not recommended!)
            request = Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; ' + \
                               'rv:91.0; ADSSO) Gecko/20100101 Firefox/91.0')
            print("Warning - Request to server does not reveal client's true identity.")
            print("          Use this option only if absolutely necessary!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError as message: # probably a syntax error
        print(f"\nCannot find requested document '{url}'")
        print(f"Error message was: {message}\n")
        return None
    except HTTPError as message: # possibly an authorisation problem
        print(f"\nAccess denied to document at URL '{url}'")
        print(f"Error message was: {message}\n")
        return None
    except URLError as message: # probably the wrong server address
        print(f"\nCannot access web server at URL '{url}'")
        print(f"Error message was: {message}\n")
        return None
    except Exception as message: # something entirely unexpected
        print("\nSomething went wrong when trying to download " + \
              f"the document at URL '{str(url)}'")
        print(f"Error message was: {message}\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError as message:
        print("\nUnable to decode document from URL " + \
              f"'{url}' as '{char_set}' characters")
        print(f"Error message was: {message}\n")
        return None
    except Exception as message:
        print("\nSomething went wrong when trying to decode " + \
              f"the document from URL '{url}'")
        print(f"Error message was: {message}\n")
        return None

    # Optionally write the contents to a local text file
    # (silently overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(f'{target_filename}.{filename_extension}',
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print(f"\nUnable to write to file '{target_filename}'")
            print(f"Error message was: {message}\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution below.
#
# Create the main window
main_window = Tk()

# Why won't this work
# I am going to lose my mind
# I have been working on this for hours
# I have tried everything
# Yay it finally works
# It Broke again

# README
# I give up on this. Instead of pulling exact time I will pull the relative time from the webpage
# I will then use the current time to calculate the time the article was uploaded
# I will then display this time in the information section
# And save it to the database
# It will lose some accuracy but it will work

# Your code goes here
import re
import datetime
from datetime import datetime, timedelta
from tkinter import Label  # Import the Label class from tkinter
# URLs for the news sources
NEWS_9NEWS = 'https://www.9news.com.au/just-in'
NEWS_AGE = 'https://www.theage.com.au/breaking-news'
NEWS_COM_AU = 'https://www.news.com.au/breaking-news'

current_datetime = datetime.now()


def update_information_section():
    selected_info_source = selected_source.get()
    message = f"You have selected an unknown source: {selected_info_source}"  # Default message
    if selected_info_source == '9news':
        message = f"You have selected {selected_info_source}\nURL: {NEWS_9NEWS}"
    elif selected_info_source == 'The Age News':
        message = f"You have selected {selected_info_source}\nURL: {NEWS_AGE}"
    elif selected_info_source == 'NEWS.COM.AU':
        message = f"You have selected {selected_info_source}\nURL: {NEWS_COM_AU}"
    information_section.config(text=message)

def confirm_button_click():
    # Clear the information section
    information_section.config(text='')
    # Needs to check the webpage and scrape it for the time and title of the latest news article on the page
    selected_info_source = selected_source.get()
    
    # 9 NEWS
    if selected_info_source == '9news':
        for label in information_section.winfo_children():
            label.destroy()
        # Download the webpage
        webpage = download(NEWS_9NEWS)
        # Find the title of the latest news article
        title_match = re.search(r'<span class="story__headline__text">(.*?)</span>', webpage)
        # Find the time of the latest news article
        time_match = re.search(r'<time class="story__time">(.*?)</time>', webpage)
        # Find the abstract of the latest news article
        abstract_match = re.search(r'<div class="story__abstract">(.*?)</div>', webpage)
        # Check if time, title and abstract are not None
        if time_match is not None and title_match is not None and abstract_match is not None:
            # Extract the matched groups
            title = title_match.group(1)
            time = time_match.group(1)
            abstract = abstract_match.group(1)
            # Display the title in larger bolded font
            title_label = Label(information_section, text=title, font=("Arial", 16, "bold"), wraplength=600)
            title_label.pack()
            # Display the abstract in regular style
            abstract_label = Label(information_section, text=abstract, wraplength=600)
            abstract_label.pack()
            text = time_match.group(1)
            time = text.split()[0]
            time = int(time)
            upload_datetime = current_datetime - timedelta(minutes=time)
            display_datetime = upload_datetime.replace(microsecond=0)
            time_label = Label(information_section, text='~' + str(display_datetime), fg="blue")
            time_label.pack()
        else:
            information_section.config(text="Could not find time, title or abstract of the article.")
    



    # THE AGE NEWS
    elif selected_info_source == 'The Age News':
        # Clear previous labels
        for label in information_section.winfo_children():
            label.destroy()
        
        # Download the webpage
        webpage = download(NEWS_AGE)
        # Find the time of the latest news article
        time_match = re.search(r'<time class="_2_zR-"[^>]*>(.*?)</time>', webpage)
        # Find the title of the latest news article
        title_match = re.search(r'<h3 class="_13KNF _2XVos"[^>]*><a[^>]*>(.*?)</a></h3>', webpage)
        # Find the abstract of the latest news article
        abstract_match = re.search(r'<p class="_3b7W- _3XEsE"[^>]*>(.*?)</p>', webpage)
        # Check if time, title and abstract matches are found
        if time_match and title_match and abstract_match:
            # Extract the matched groups
            time = time_match.group(1)
            title = title_match.group(1)
            abstract = abstract_match.group(1)
            # Display the title in larger bolded font
            title_label = Label(information_section, text=title, font=("Arial", 16, "bold"), wraplength=600)
            title_label.pack()
            # Display the abstract in normal font
            abstract_label = Label(information_section, text=abstract, wraplength=600)
            abstract_label.pack()
            # Display the time in a different color
            text = time_match.group(1)
            time = text.split()[0]
            time = int(time)
            upload_datetime = current_datetime - timedelta(minutes=time)
            display_datetime = upload_datetime.replace(microsecond=0)
            time_label = Label(information_section, text='~' + str(display_datetime), fg="blue")
            time_label.pack()
        else:
            information_section.config(text="Could not find time, title or abstract of the article.")



    # NEWS.COM.AU
    elif selected_info_source == 'NEWS.COM.AU':
        for label in information_section.winfo_children():
            label.destroy()
        # Download the webpage
        webpage = download(NEWS_COM_AU)
        # Find the time of the latest news article
        time_match = re.search(r'<time class="storyblock_datetime g_font-base-s"[^>]*>(.*?)</time>', webpage)
        # Find the title of the latest news article
        title_match = re.search(r'<a class="storyblock_title_link"[^>]*>(.*?)</a>', webpage)
        # Find the abstract of the latest news article
        abstract_match = re.search(r'<p class="storyblock_standfirst g_font-body-s"[^>]*>(.*?)</p>', webpage)
        # Check if time, title and abstract matches are found
        if time_match and title_match and abstract_match:
            # Extract the matched groups
            time = time_match.group(1)
            title = title_match.group(1)
            abstract = abstract_match.group(1)
            # Display the title in larger bolded font
            title_label = Label(information_section, text=title, font=("Arial", 16, "bold"), wraplength=600)
            title_label.pack()
            # Display the abstract in normal font
            abstract_label = Label(information_section, text=abstract, wraplength=600)
            abstract_label.pack()
            text = time_match.group(1)
            time = text.split()[0]
            time = int(time)
            upload_datetime = current_datetime - timedelta(minutes=time)
            display_datetime = upload_datetime.replace(microsecond=0)
            time_label = Label(information_section, text='~' + str(display_datetime), fg="blue")
            time_label.pack()
        else:
            information_section.config(text="Could not find time, title or abstract of the article.")

# def save_to_database():


def display_button_click():
    # Clear the information section
    information_section.config(text='')
    #Need to open the webpage in the browser
    selected_info_source = selected_source.get()
    if selected_info_source == '9news':
        urldisplay(NEWS_9NEWS)
    elif selected_info_source == 'The Age News':
        urldisplay(NEWS_AGE)
    elif selected_info_source == 'NEWS.COM.AU':
        urldisplay(NEWS_COM_AU)


def apply_button_click():
    # Clear the information section
    information_section.config(text='')
    reliability_rating = reliability_slider.get()
    current_text = information_section.cget("text")
    information_section.config(text=current_text)
    # Get the selected source
    selected_info_source = selected_source.get()  # Change the variable name here
    
    # Check if a source has been selected
    if not selected_info_source:  # And here
        information_section.config(text="No source selected!")
        return
    
    # Get the labels generated by the confirm button click function
    labels = information_section.winfo_children()
    
    # Check if any labels are present
    if not labels:
        information_section.config(text="No information available!")
        return
    
    # Extract the information from the labels
    headline = labels[0].cget("text")
    time = labels[2].cget("text")
    
    # Save the extracted information to the database
    conn = connect('reliability_ratings.db')
    c = conn.cursor()
    c.execute("INSERT INTO ratings (news_source, headline, dateline, rating) VALUES (?, ?, ?, ?)", (selected_info_source, headline, time, reliability_rating))  # And here
    conn.commit()
    conn.close()

# Configure tkinter window
main_window.title('News Check and Reliabilty Rating System')
main_window.geometry('900x600')
main_window.configure(bg='slate grey')

# Add a section to display the information
information_section = Label(main_window, text='Information Section', bg='silver')
information_section.grid(row=1, column=1, columnspan=2, sticky='nsew', padx=10, pady=10)
information_section.config(width=60, height=10, relief='solid', bd=2, padx=5, pady=5)


# Add a section to display the sources of information
sources_of_information = Label(main_window, text='Sources of Information', bg='silver')
sources_of_information.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
sources_of_information.config(width=30, height=10, anchor='n', relief='solid', bd=2, padx=5, pady=5)

# Create a frame inside the 'sources_of_information' label
frame = Frame(sources_of_information, bg='silver')
frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=30)

# Create a StringVar to track the selected radio button
selected_source = StringVar()

# Create the radio buttons with the 'variable' option set to 'selected_source' and 'indicatoron' set to 1
Radiobutton(frame, text='9news', variable=selected_source, value='9news', bg='light grey', indicatoron=0, command=update_information_section).grid(row=1, column=0, sticky='w', padx=10, pady=10)
Radiobutton(frame, text='The Age News', variable=selected_source, value='The Age News', bg='light grey', indicatoron=0, command=update_information_section).grid(row=2, column=0, sticky='w', padx=10, pady=10)
Radiobutton(frame, text='NEWS.COM.AU', variable=selected_source, value='NEWS.COM.AU', bg='light grey', indicatoron=0, command=update_information_section).grid(row=3, column=0, sticky='w', padx=10, pady=10)

# Place the buttons inside the frame
confirm_button = Button(frame, text='Confirm', bg='light grey', command=confirm_button_click)
confirm_button.grid(row=4, column=0, sticky='w', padx=10, pady=10)

display_button = Button(frame, text='Display', bg='light grey', command=display_button_click)
display_button.grid(row=5, column=0, sticky='w', padx=10, pady=10)

reliabilty = Label(main_window, bg='silver', text='Reliability Rating', anchor='n')
reliabilty.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
reliabilty.config(width=30, height=10, relief='solid', bd=2, padx=5, pady=5)
reliabilty.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
reliabilty.config(width=30, height=10, relief='solid', bd=2, padx=5, pady=5)

frame = Frame(reliabilty, bg='silver')
frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=30)

# Slider for the reliability of the source, range from 1-5 apply the rating
reliability_slider = Scale(frame, from_=1, to=5, orient=HORIZONTAL, bg='light grey')
reliability_slider.grid(row=2, column=0, sticky='w', padx=10, pady=10)

# Add a button to apply the rating
apply_button = Button(frame, text='Apply', bg='light grey', command=apply_button_click)
apply_button.grid(row=3, column=0, sticky='w', padx=10, pady=10)


# Import the image
image = PhotoImage(file='Fact-Checking-Verification-771x386.png')

# Create a label to display the image
image_label = Label(main_window, image=image)
image_label.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)

# Create a label to display the image
image_label = Label(main_window, image=image)
image_label.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)

# Add faint colored text underneath the image
image_text = Label(main_window, text="https://gijn.org/resource/fact-checking-verification/", fg="gray", font=("Arial", 8))
image_text.grid(row=3, column=2, sticky='nsew', padx=10, pady=5)

# Start the event loop to detect user inputs
main_window.mainloop()
