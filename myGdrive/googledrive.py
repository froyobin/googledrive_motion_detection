from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


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


if __name__ == "__main__":
    this_drive = MyGoogleDrive()
    # this_drive.upload_file("hello", '/home/pi/test.png')
    file_id = this_drive.get_file_id('video_camera')
    this_drive.upload_file(file_id, "pic.png", "/home/pi/test.png")