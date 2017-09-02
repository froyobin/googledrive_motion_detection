from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time

class MyGDrive:
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)

    def get_file_id(self, filename):
        file_list = self.drive.ListFile({'q': "'root' in parents and "
                                          "trashed=false"}).GetList()
        thisfile = None

        for file in file_list:
            if file['title'] == filename:
                print file['id']
                thisfile = file

        if thisfile is None:
            return None
        else:
            return thisfile['id']

    def upload_file(self, folderid, filename, filepath):

        metadata =  {'title':filename, "parents": [{"kind": "drive#fileLink",
                                      "id": folderid}]}
        file = self.drive.CreateFile(metadata)
        file.SetContentFile(filepath)
        file.Upload() # Upload the file.
        return file['id']

    def delete_file(self, fileid):
        dfile = self.drive.CreateFile({'id': fileid})
        file_name = dfile['title']
        dfile.Delete()
        print "delete: " + file_name

    def query_exit_file(self, filename):
        file_list = self.drive.ListFile(
            {'q': "title = '%s' and trashed=false" % filename}).GetList()
        if len(file_list) == 0:
            return None
        else:
            return file_list[0]

if __name__ == "__main__":
    this_drive = MyGDrive()
    # this_drive.upload_file("hello", '/home/pi/test.png')
    file_id = this_drive.get_file_id('video_camera')
    uploaded_id = this_drive.upload_file(file_id, "pic.png",
                                         "/home/pi/test.png")
    # time.sleep(10)
    # this_drive.delete_file(uploaded_id)
    file = this_drive.query_exit_file("start_monitor.txt")
    if file is not None:
        print file['title']