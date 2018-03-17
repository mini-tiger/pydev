# coding:utf-8
from optparse import OptionParser

parser = OptionParser(usage="%prog [-f] [-q]", version="%prog 1.0")
'''
G:\pydev\pydev\modelss\optparse>python sample.py --version
sample.py 1.0

'''

parser.add_option("-f", "--file",
                  dest="filename",
                  type='string',  # "string" or "int"
                  help="write report to FILE",
                  metavar="FILE")
parser.add_option("-q", "--quiet",
                  action="store_true",  ##必须输入-q,否则报错 ,store_true,store_const 、append 、count 、callback 
                  dest="verbose",
                  # default=True,  #不用输入-q 默认是True
                  help="don't print status messages to stdout")



if __name__ == '__main__':
    options, args = parser.parse_args()
    filename = options.filename  ##获取 dest filename,

    verbose = options.verbose
    if not verbose:
	    parser.error("must verbose") #的异常处理方法还不能满足要求，你可能需要继承 OptionParser 类，并重载 exit() 和 erro() 方法
   
    print 'filename : {} ,type: {}'.format(filename, type(filename))
    print 'verbaose : {} ,type: {}'.format(verbose, type(verbose))
    # print options.read_file

    print u'额外输入列表:{}'.format(args)  # 指定以外的 参数 输入
    # print dir(parser)
    '''
    G:\pydev\pydev\modelss\optparse>python sample.py -h
    Usage: sample.py [-f] [-q]
    
    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -f FILE, --file=FILE  write report to FILE
      -q, --quiet           don't print status messages to stdout
    '''

    '''
  G:\pydev\pydev\modelss\optparse>python sample.py -f 111 -q 111,a=1
	filename : 111 ,type: <type 'str'>
	verbaose : 1 ,type: <type 'int'>
	额外输入列表:['111,a=1']  
    '''


'''

G:\pydev\pydev\modelss\optparse>python sample.py -f 111
Usage: sample.py [-f] [-q]

sample.py: error: must verbose
'''