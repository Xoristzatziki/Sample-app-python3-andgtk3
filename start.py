#!/usr/bin/python3

#Copyright Ηλιάδης Ηλίας, 2018
#v.0.0.1
# contact http://gnu.kekbay.gr/sampleapp/  -- mailto:iliadis@kekbay.gr
#
# This file is part of sampleapp.
#
# This is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3.0 of the License, or (at your option) any
# later version.
#
# It is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along
# with the source code.  If not, see <http://www.gnu.org/licenses/>.

import os, sys, signal

import subprocess
import tempfile

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GLib

import locale
from locale import gettext as _

VERSION = '0.0.12'
APPNAME = 'Sample app'
APPDOMAIN = 'sampleapp'

class AboutBox:
    def __init__(self, theApp):
        aboutdialog = Gtk.AboutDialog()
        aboutdialog.set_program_name( _(theApp.appName) )
        aboutdialog.set_version(theApp.appName  + 'v.' + theApp.appVersion + ' ')
        with open(os.path.join(theApp.working_dir, '_data', 'AUTHORS'), mode='rt', encoding='utf-8') as f:
            aboutdialog.set_authors(f.readlines())
        with open(os.path.join(theApp.working_dir, '_data', 'COPYRIGHT'), mode='rt', encoding='utf-8') as f:
            aboutdialog.set_copyright(f.read())
        with open(os.path.join(theApp.working_dir, '_data', 'COMMENTS'), mode='rt', encoding='utf-8') as f:
            aboutdialog.set_comments(f.read())
        with open(os.path.join(theApp.working_dir, '_data', 'TRANSLATORS'), mode='rt', encoding='utf-8') as f:
            aboutdialog.set_translator_credits(f.read())
        aboutdialog.set_transient_for(theApp.my_main_window)
        aboutdialog.set_logo(theApp.appIcon)
        aboutdialog.run()
        aboutdialog.destroy()

class clsWindowHandler():
    def __init__(self, theApp):
        self.we_can_exit_now = False
        self.return_parameter = None
        self.App = theApp
        self.App.mybuilder.connect_signals(self)
        self._window = self.App.my_main_window
        self._window.set_icon(self.App.appIcon)
        self._window.set_title(_(APPNAME))

        self.builder('lblversion').set_label(_('Version:') + ' ' + self.App.appVersion + ' ')
        self.argsdict = {}
        self.new_with_dummy_rows()
        self.pid = None
        self.tw_out = self.builder('textview1')
        self.tw_err = self.builder('textview2')
        set_object_style(self.tw_out, 'background-color', 'black')
        set_object_style(self.tw_out, 'color', 'green')

    def builder(self, a_builder_id):
        return self.App.mybuilder.get_object(a_builder_id)

    def run(self):
        #now we can show the window
        self._window.show_all()
        #loop eternaly
        while True:
            #if we want to exit
            if self.we_can_exit_now:
                #print('we_can_exit_now')
                #break the loop
                break
            #else...
            #give others a change...
            while Gtk.events_pending():
                Gtk.main_iteration()
        #we can now return to calling procedure
        #can return any variable we want
        #or we can check the widgets and/or variables
        #from inside calling procedure
        #print('from abstract',self.returnparameter)
        return self.return_parameter

    def on_mainWindow_hide(self, *args):
        self.we_can_exit_now = True

    def on_bexit_clicked(self, widget, *args):
        #self.on_windowMain_destroy(*args)
        self._window.set_transient_for()
        self._window.set_modal(False)
        self._window.hide()

    def on_babout_clicked(self, widget, *args):
        app = AboutBox(self.App)

    def on_brun_clicked(self, widget, *args):
        #TODO
        NotYet(self._window,_(self.App.appName))

    def on_bsave_clicked(self, widget, *args):
        #TODO
        NotYet(self._window,_(self.App.appName))

    def on_bload_clicked(self, widget, *args):
        #TODO
        NotYet(self._window,_(self.App.appName))

    def choose_a_file(self, widget, *args):
        dialog = Gtk.FileChooserDialog(_("Please choose a file"), self._window,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        #dialog.set_current_folder(self.CS.lastpathfrom)
        oldpath = os.path.dirname(args[0].get_text())
        if os.path.exists(oldpath):
            dialog.set_current_folder(oldpath)
        add_some_filters(dialog)

        response = dialog.run()
        filename = dialog.get_filename()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            args[0].set_text(filename)

    def change_state(self, widget, *args):
        #label with space between hyphens, for visual clarification.
        #requires more coding, but makes interface more readable...
        widget.set_property('label','- -' if widget.get_active() else '-')

    def add_a_row(self):
        xcounter = len(self.argsdict)

        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        label = Gtk.Label(_('arg') + str(xcounter))
        hbox1.pack_start(label, False, False, 0)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        tbutton = Gtk.ToggleButton('-')
        tbutton.connect('clicked', self.change_state)
        hbox.pack_start(tbutton, False, False, 0)
        entry1 = Gtk.Entry()
        hbox.pack_start(entry1, False, False, 0)
        entry2 = Gtk.Entry()
        hbox.pack_start(entry2, True, True, 0)
        button = Gtk.Button('...')
        button.connect('clicked', self.choose_a_file, entry2)
        hbox.pack_start(button, False, False, 0)
        vbox.pack_start(hbox, True, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        rb1 = Gtk.RadioButton(_('as is'))
        rb1.set_name('1')
        hbox.pack_end (rb1, False, False, 0)
        rb2 = Gtk.RadioButton.new_with_label_from_widget(rb1, _('bash quoted'))
        rb2.set_name('2')
        hbox.pack_end (rb2, False, False, 0)
        rb3 = Gtk.RadioButton.new_with_label_from_widget(rb1, _('single quoted'))
        rb3.set_name('3')
        hbox.pack_end (rb3, False, False, 0)
        rb4 = Gtk.RadioButton.new_with_label_from_widget(rb1, _('double quoted'))
        rb4.set_name('4')
        hbox.pack_end (rb4, False, False, 0)
        label = Gtk.Label(_('param will be:'))
        hbox.pack_end (label, False, False, 0)
        vbox.pack_start(hbox, True, True, 0)
        hbox1.pack_start(vbox, True, True, 0)

        row = Gtk.ListBoxRow()
        row.add(hbox1)

        box_for_args = self.builder('listboxforargs')
        box_for_args.add(row)
        self.argsdict[xcounter] = {'arg':entry1, 'val':entry2, 'tb':tbutton, 'ob':rb1}

    def clear_box(self):
        allchildren = self.builder('listboxforargs').get_children()
        for achild in allchildren[:]:
            achild.destroy()

    def new_with_dummy_rows(self):
        self.argsdict.clear()
        self.clear_box()
        howmany = int(self.builder('adjustmentofargs').get_value())
        for x in range(howmany):
            self.add_a_row()
        #refresh window...
        self._window.show_all()

    def on_entrycommandname_changed(self, widget, *args):
        self.show_man_page()
        self.create_command()

    def create_command(self):
        thecommand = self.builder('entrycommandname').get_text()
        for val in self.argsdict:
            thearg = self.argsdict[val]['arg'].get_text()
            theval = self.argsdict[val]['val'].get_text()
            if len(thearg):
                thecommand += ' ' + single_or_double(self.argsdict[val]['tb'].get_property('label')) + thearg
            if len(theval):
                selectionint = int(resolve_radio(self.argsdict[val]['ob']))
                if selectionint == 1:#as is
                    thecommand += ' ' + theval
                elif selectionint == 2:#bash quoted
                    thecommand += ' ' + sh_escape(theval)
                elif selectionint == 3:#single quoted
                    thecommand += " '" + theval + "'"
                else: #one radio button must be selected. Hence the last is: double quoted
                    thecommand += ' "' + theval + '"'

        self.builder('labelforcommand').set_label(thecommand)

    def on_adjustmentofargs_changed(self, widget, *args):
        #TODO: do not clear old if not necessary, just add new or remove from the end
        self.new_with_dummy_rows()

    def startpinner(self):
        self.builder('spinner1').start()

    def stopspinner(self):
        self.builder('spinner1').stop()

    def update_progress(self, data=None):
        #self.progress.pulse()
        #dummy for me
        return True

    #based on https://stackoverflow.com/questions/20760535/button-stop-cancel-progressbar-from-subprocess-pygtk/20790769#20790769
    def spawn_man_read(self):
        params = ['man', self.builder('entrycommandname').get_text()]

        def scroll_to_end(textview):
            i = textview.props.buffer.get_end_iter()
            mark = textview.props.buffer.get_insert()
            textview.props.buffer.place_cursor(i)
            textview.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)

        def write_to_textview(io, condition, tw):
            if condition is GLib.IO_HUP:
                GLib.source_remove(self.source_id_out)
                GLib.source_remove(self.source_id_err)
                self.builder('spinner1').stop()
                return False

            line = io.readline()
            tw.props.buffer.insert_at_cursor(line)
            #time consumer, but good for attraction:
            #scroll_to_end(tw)

            while Gtk.events_pending():
                Gtk.main_iteration_do(False)

            return True

        self.pid, stdin, stdout, stderr = GLib.spawn_async(params,
            flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            standard_output=True,
            standard_error=True)

        self.builder('spinner1').start()

        io = GLib.IOChannel(stdout)
        err = GLib.IOChannel(stderr)

        self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                                 write_to_textview,
                                 self.tw_out,
                                 priority=GLib.PRIORITY_HIGH)

        self.source_id_err = err.add_watch(GLib.IO_IN|GLib.IO_HUP,
                                 write_to_textview,
                                 self.tw_err,
                                 priority=GLib.PRIORITY_HIGH)

        timeout_id = GLib.timeout_add(100, self.update_progress)

        def closure_func(pid, status, data):
            GLib.spawn_close_pid(pid)
            GLib.source_remove(timeout_id)
            self.builder('spinner1').stop()
            self.pid = None

        GLib.child_watch_add(self.pid, closure_func, None)

    def show_man_page(self):
        #stop older "spawns"
        if self.pid:
            os.kill(self.pid, signal.SIGTERM)
            self.pid = None
        self.tw_out.props.buffer.set_text('')
        self.tw_err.props.buffer.set_text('')
        self.spawn_man_read()

class Application:
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.appVersion = VERSION
        #if we have a file named debug, get version from the directory name
        #else use the one already provided (in the begging of the file as VERSION)
        if os.path.exists(os.path.join(working_dir, 'debug')):
            forversion = os.path.basename(self.working_dir)
            if len(forversion) > 2 and (forversion.count('.') == 3):
                self.appVersion = forversion[2:]
        self.appName = APPNAME
        locale.bindtextdomain(APPDOMAIN, os.path.join(self.working_dir, '_locale'))
        locale.textdomain(APPDOMAIN)
        self.appIcon = GdkPixbuf.Pixbuf.new_from_file(os.path.join(self.working_dir, '_icons', "logo.png"))
        self.appUserDir = os.getenv('USERPROFILE') or os.getenv('HOME')

        self.mybuilder = Gtk.Builder()
        self.mybuilder.add_from_file(os.path.join(self.working_dir, 'mainwindow.glade'))
        self.my_main_window = self.mybuilder.get_object("mainWindow")

        self.thewindow = clsWindowHandler(self)

#general function
def add_some_filters( dialog):
    filter_any = Gtk.FileFilter()
    filter_any.set_name(_("All files"))
    filter_any.add_pattern("*")
    dialog.add_filter(filter_any)

    filter_video = Gtk.FileFilter()
    filter_video.set_name(_("Video files"))
    filter_video.add_mime_type("video/mp4")
    filter_video.add_mime_type("video/x-matroska")
    filter_video.add_mime_type("video/x-msvideo")
    dialog.add_filter(filter_video)

def set_object_style(theobject, var, val):
    css = '''*{''' + var + ''':''' + val + ''';}'''
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(css.encode('utf-8'))
    context = theobject.get_style_context()
    context.add_provider(style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

#based on https://stackoverflow.com/questions/8812389/gtk-how-do-i-find-which-radio-button-is-selected
def resolve_radio(master_radio):
    active = next((
        radio for radio in
        master_radio.get_group()
        if radio.get_active()
    ))
    return active.get_name()

def sh_escape(s):
   return s.replace("(","\\(").replace(")","\\)").replace(" ","\\ ")

def single_or_double(thestr):
    return ("-" if thestr == '-' else '--')

def NotYet(appwindow, appname):
    dialog = Gtk.MessageDialog(appwindow, 0, Gtk.MessageType.INFO,
        Gtk.ButtonsType.OK, _("NOT YET!"))
    dialog.format_secondary_text(_("Not yet implemented!"))
    dialog.set_title(appname)
    #dialog.set_transient_for(appwindow)
    dialog.run()
    dialog.destroy()

def main(working_dir):
    myApp = Application(working_dir)
    response = myApp.thewindow.run()
    sys.exit(response)

#if it is called from command line the "__name__" will be: "__main__"
#so run whatever is here.
#if it is included using "import" this will never run.
if __name__ == "__main__":
    realfile = os.path.realpath(__file__)
    working_dir = os.path.dirname(os.path.abspath(realfile))
    #run the application
    main(working_dir)

