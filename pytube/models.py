from __future__ import unicode_literals
from os.path import normpath
from urllib2 import urlopen

class Video(object):
    """
    Class representation of a single instance of a YouTube video.
    """
    def __init__(self, url, filename, **attributes):
        """
        Define the variables required to declare a new video.

        Keyword arguments:
        extention -- The file extention the video should be saved as.
        resolution -- The broadcasting standard of the video.
        url -- The url of the video. (e.g.: youtube.com/watch?v=..)
        filename -- The filename (minus the extention) to save the video.
        """

        self.url = url
        self.filename = filename
        self.__dict__.update(**attributes)
        
    def download(self, path=None, chunk_size=8*1024):
        """
        Downloads the file of the URL defined within the class
        instance.

        Keyword arguments:
        path -- Destination directory
        chunk_size -- File size (in bytes) to write to buffer at a time
        (default: 8 bytes).
        """

        path = (normpath(path) + '/' if path else '')
        response = urlopen(self.url)
        with open(path + self.filename, 'wb') as dst_file:
            meta_data = dict(response.info().items())
            file_size = int(meta_data.get("Content-Length") or
                            meta_data.get("content-length"))
            self._bytes_received = 0
            while True:
                self._buffer = response.read(chunk_size)
                if not self._buffer:
                    break
                
                self._bytes_received += len(self._buffer)
                dst_file.write(self._buffer)
                percent = self._bytes_received * 100. / file_size
                status = r"%10d  [%3.2f%%]" % (self._bytes_received, percent)
                status = status + chr(8) * (len(status) + 1)
                print status,

    def __repr__(self):
        """A cleaner representation of the class instance."""
        return "<Video: %s (.%s) - %s>" % (self.video_codec, self.extension,
                                           self.resolution)

    def __lt__(self, other):
        if type(other) == Video:
            v1 = "%s %s" % (self.extension, self.resolution)
            v2 = "%s %s" % (other.extension, other.resolution)
            return (v1 > v2) - (v1 < v2) < 0
