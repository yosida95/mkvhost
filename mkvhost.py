#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import shutil
import fcntl
import re


def mkvhost():
    Conf_Dir = '/etc/httpd/conf.d'
    Conf_Template = '/var/www/mkvhost/conf.tpl'
    Init_HTML = '/var/www/mkvhost/index.html'

    host = sys.argv[1].lower()
    conf = os.path.join(Conf_Dir, '%s.conf' % host)
    admin = sys.argv[2]
    root_dir = os.path.normpath(sys.argv[3])
    if os.path.exists(conf):
        is_continue = raw_input(u'すでに設定ファイルが存在します。上書きしますか？ (y/N): ')
        if is_continue == '' or is_continue in ('n', 'N', 'no', 'No', 'NO'):
            print u'中断しました'
            exit(0)

    if not os.path.exists(root_dir):
        is_mkdir = raw_input(u'%sが存在しません。作成しますか？(Y/n): ' % (root_dir))
        if is_mkdir in ('y', 'Y', 'yes', 'Yes', 'YES') or is_mkdir == '':
            os.makedirs(root_dir)
            shutil.copyfile(Init_HTML, '%s/index.html' % root_dir)

    mkconf = open(conf, 'w')
    fcntl.flock(mkconf.fileno(), fcntl.LOCK_EX)
    template = open(Conf_Template, 'r')
    text = template.read() % {'host': host, 'admin': admin, 'root_dir': root_dir}
    mkconf.write(text)
    template.close()
    fcntl.flock(mkconf.fileno(), fcntl.LOCK_UN)
    mkconf.close()
    os.system('/etc/init.d/httpd reload')


def rmvhost():
    Conf_Dir = '/etc/httpd/conf.d'

    host = sys.argv[1]
    conf_path = os.path.join(Conf_Dir, '%s.conf' % host)
    if os.path.exists(conf_path):
        is_continue = raw_input(u'%sの設定を削除します。続行しますか？(y/N): ' % host)
        if is_continue == '' or is_continue in ('n', 'N', 'no', 'No', 'NO'):
            print u'中止しました。'
            exit(0)
        conf = open(conf_path, 'r')
        match = re.search(r'DocumentRoot ([^\r\n]+)[\r\n]*', conf.read())
        conf.close()
        root_dir = match.group(1) if match else ''
        if not root_dir == '' and os.path.exists(root_dir):
            is_delete = raw_input(u'ディレクトリ: %sを削除しますか？(y/N): ' % (root_dir))
            if is_delete in ('yes', 'Y', 'y', 'YES', 'Yes'):
                os.rmdir(os.path.normpath(root_dir))
        os.remove(conf_path)
        os.system('/etc/init.d/httpd reload')
    else:
        print u'該当の設定が存在しません。'
        exit(0)

if __name__ == '__main__':
    if len(sys.argv) == 4:
        mkvhost()
    elif len(sys.argv) == 2:
        rmvhost()
    else:
        print u'引数が不十分です'
