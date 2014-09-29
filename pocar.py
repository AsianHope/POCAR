#!/bin/python
#taken from http://www.yolinux.com/TUTORIALS/PyGTK.html
#testing forks

import pygtk
import gtk
import fileinput
import errno, sys

class MyProgram:
    def __init__(self):

        self.parents= {}
        try:
            f = open('parents.csv')
        except:
           parent = None
           md = gtk.MessageDialog(parent, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                    gtk.BUTTONS_CLOSE, "Can't open file!")
           md.run()
           sys.exit(1)
        for line in f:
            line = line.strip()
            info = line.split(',')
            pid = info[0]
            student_list = []
            i = 0

            for item in info:
                if(i>=2): #parent_id, name, student1, student2, student3... student9
                    student_list.append(info[i])
                i+=1

            self.parents[pid] = student_list

        #create a new window
        self.app_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.app_window.fullscreen()
        self.app_window.set_title("POCAR")

        #change color of window??
        #self.green = gtk.gdk.color_parse('green')
        #self.red = gtk.gdk.color_parse('red')
        #self.app_window.modify_bg(gtk.STATE_NORMAL,self.green)

        #add entry and search fields
        self.entry = gtk.Entry()
        self.button_search = gtk.Button("Search")
        self.button_search.connect("clicked", self.search_button_clicked, "3")
        self.button_search.set_size_request(50,50)

        #add image display area
        self.student_pic = gtk.EventBox()
        self.student_id= gtk.EventBox()

        spacer1 = gtk.EventBox()
        spacer2 = gtk.EventBox()

        #self.label=gtk.Label("Please scan a card")
        #init = '<span background="gray"><span size="128000">XXX</span>\n<span size="64000">Please scan a card</span></span>'
        #self.label.set_markup(init)
        #self.student_id.add(self.label)

        pixbuf = gtk.gdk.pixbuf_new_from_file("static/OK.JPG")
        scaled_buf = pixbuf.scale_simple(177,266,gtk.gdk.INTERP_BILINEAR)

        self.pickup_students = ['0']*9 #seed the list with the size we want
        for i in range(0,9):
            self.pickup_students[i] = gtk.Image()
            self.pickup_students[i].set_from_pixbuf(scaled_buf)
            self.pickup_students[i].show()

        self.label=gtk.Table(3,3,True)
        self.label.attach(self.pickup_students[0],0,1,0,1)
        self.label.attach(self.pickup_students[1],1,2,0,1)
        self.label.attach(self.pickup_students[2],2,3,0,1)

        self.label.attach(self.pickup_students[3],0,1,1,2)
        self.label.attach(self.pickup_students[4],1,2,1,2)
        self.label.attach(self.pickup_students[5],2,3,1,2)

        self.label.attach(self.pickup_students[6],0,1,2,3)
        self.label.attach(self.pickup_students[7],1,2,2,3)
        self.label.attach(self.pickup_students[8],2,3,2,3)

        vbox = gtk.VBox()
        student_info = gtk.HBox()
        controls = gtk.VBox()
        bottom_area = gtk.HBox()

        controls.pack_start(self.entry,fill=False)
        controls.pack_start(self.button_search,fill=False)

        student_info.pack_start(self.student_pic,fill=False)
        #student_info.pack_start(self.student_id,fill=False)
        student_info.pack_start(self.label, True, True, 0)
        
        bottom_area.pack_start(spacer1)
        bottom_area.pack_start(controls)
        bottom_area.pack_start(spacer2)

        vbox.pack_start(student_info)
        vbox.pack_start(bottom_area)
        self.app_window.add(vbox)

        self.image = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("static/logo.png")
        scaled_buf = pixbuf.scale_simple(472,709,gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(scaled_buf)
        self.image.show()

        self.student_pic.add(self.image)

        self.button_search.set_flags(gtk.CAN_DEFAULT)
        self.button_search.grab_default()
        self.entry.set_activates_default(True)
        self.app_window.set_focus(self.entry)

        self.app_window.show_all()

        return

    def search_button_clicked(self, widget, data=None):
        for i in range(0,9):
            #make sure all pictures are reset
            pixbuf = gtk.gdk.pixbuf_new_from_file("static/NA.JPG")
            scaled_buf = pixbuf.scale_simple(177,266,gtk.gdk.INTERP_BILINEAR)
            self.pickup_students[i].set_from_pixbuf(scaled_buf)


        #intersting stuff goes here
        #grab pid
        pid = self.entry.get_text()

        #do a lookup for the name
        try:
            names = self.parents[pid]
        except KeyError:
            names = "NA"

        #display the result
        #successful result
        #result = '<span background="green"><span size="128000">'+pid+'</span>\n<span size="64000">'+name+'</span></span>'

        #if name == 'NA':
        #    result = '<span background="red"><span size="128000">'+pid+'</span>\n<span size="64000">No Lunch!</span></span>'
            #pid = names
            #self.app_window.modify_bg(gtk.STATE_NORMAL, self.red)
        #self.label.set_markup(result)
        #self.label.show()

        #load pictures
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file("resource/"+pid+".JPG")
            scaled_buf = pixbuf.scale_simple(472,709,gtk.gdk.INTERP_BILINEAR)
            self.image.set_from_pixbuf(scaled_buf)
            
            i = 0
            for sid in names:
                try:
                    pixbuf = gtk.gdk.pixbuf_new_from_file("resource/"+sid+".JPG")
                    scaled_buf = pixbuf.scale_simple(177,266,gtk.gdk.INTERP_BILINEAR)
                    self.pickup_students[i].set_from_pixbuf(scaled_buf)
                except: break
                i+=1
        except:
            pixbuf = gtk.gdk.pixbuf_new_from_file("static/OK.JPG")
            scaled_buf = pixbuf.scale_simple(472,709,gtk.gdk.INTERP_BILINEAR)
            self.image.set_from_pixbuf(scaled_buf)



        #clear entry box and reset focus
        self.entry.set_text('')
        self.app_window.set_focus(self.entry)
        self.app_window.show()
def main():
    gtk.main()
    return 0

if __name__=="__main__":
    MyProgram()
    main()

