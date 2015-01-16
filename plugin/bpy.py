#!/usr/bin/python2
# Copyright (C) 2013 by Yu-Jie Lin
# Copyright (C) 2014 by Konstantin Mescheryakov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import vim
import os
import imp
from bpy.handlers import handlers
from bpy.services import find_service, services
import traceback

def load_config(path_to_credentials):
    _mod_data = imp.find_module("brc", [path_to_credentials])
    try:
        rc = imp.load_module("brc", *_mod_data)
    finally:
        if _mod_data[0]:
            _mod_data[0].close()
    return rc


def find_credentials():
    filename = vim.current.buffer.name
    path, _ = os.path.split(filename)
    while path != '/':
        path, _ = os.path.split(path)
        if os.path.exists(os.path.join(path, "brc.py")):
                return path
    raise IOError("Failed to open credentials")


def post():
    path_to_credentials = find_credentials()
    os.chdir(path_to_credentials)
    service_options = {}
    rc = load_config(path_to_credentials)
    if rc:
        if hasattr(rc, 'handlers'):
            for name, handler in rc.handlers.items():
                if name in handlers:
                    handlers[name].update(handler)
            else:
                handlers[name] = handler.copy()
        if hasattr(rc, 'services'):
            for name, service in rc.services.items():
                if name in services:
                    services[name].update(service)
            else:
                services[name] = service.copy()
        if hasattr(rc, 'service'):
            service = rc.service
        if hasattr(rc, 'service_options'):
            service_options.update(rc.service_options)
    service = find_service(service, service_options, vim.current.buffer.name)
    service.post()


vim.command("silent write")
cwd = os.getcwd()
cursor = vim.current.window.cursor
try:
    post()
    vim.command("silent edit!")
    vim.command("silent redraw!")
    vim.command("echo 'Post submitted'")
except Exception as e:
    traceback.print_exc()
    print(e.__class__)
    print(e.message)
os.chdir(cwd)
vim.current.window.cursor = cursor
