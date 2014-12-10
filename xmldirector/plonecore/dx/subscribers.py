# -*- coding: utf-8 -*-

################################################################
# xmldirector.plonecore
# (C) 2014,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

import uuid
import plone.api
from zope.component import getUtility
from xmldirector.plonecore.interfaces import IWebdavHandle
from xmldirector.plonecore.dx import util


def removal_handler(obj, event):
    """ Remove related XML content if a Dexterity content object
        is being deleted.
    """

    if not util.is_xml_content(event.object):
        return

    handle = getUtility(IWebdavHandle).webdav_handle()
    plone_uid = plone.api.portal.get().getId()
    storage_dir = util.get_storage_path(event.object)
    storage_parent_dir = util.get_storage_path_parent(event.object)
    handle.removedir(storage_dir, False, True)
    if handle.isdirempty(storage_parent_dir):
        handle.removedir(storage_parent_dir, False, True)


def copied_handler(obj, event):
    """ Copy XML resources to new object """

    # original and copied Dexterity object
    copied = event.object
    original = event.original

    # Is this Dexterity content object related to XML resources?
    if not util.is_xml_content(copied):
        return

    # create a new storage id 
    if original.__xml_storage_id__ == copied.__xml_storage_id__:
        copied.__xml_storage_id__ = str(uuid.uuid4())

        # an copy over XML content from original content object
        handle = getUtility(IWebdavHandle).webdav_handle()
        plone_uid = plone.api.portal.get().getId()
        storage_dir_original = '{}/{}/{}'.format(plone_uid, original.__xml_storage_id__[-4:], original.__xml_storage_id__)
        storage_dir_copied = '{}/{}/{}'.format(plone_uid, copied.__xml_storage_id__[-4:], copied.__xml_storage_id__)
        storage_dir_copied_parent = '{}/{}'.format(plone_uid, copied.__xml_storage_id__[-4:])
        handle.makedir(storage_dir_copied_parent, True, True)
        handle.copydir(storage_dir_original, storage_dir_copied)
