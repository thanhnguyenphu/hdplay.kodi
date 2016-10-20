#!/usr/bin/python
#coding=utf-8

import xbmc, xbmcaddon

addon = xbmcaddon.Addon(id='plugin.video.tnp.hdplay')

if addon.getSetting('autostart') == 'true':
	xbmc.executebuiltin("RunAddon(plugin.video.tnp.hdplay)")