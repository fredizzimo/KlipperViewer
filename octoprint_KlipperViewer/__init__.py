# Viewer for Klipper toolpaths
# Copyright (C) 2019  Fred Sundvik
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# coding=utf-8
from __future__ import absolute_import
from .serial_parser import SerialParser
import flask

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class KlipperviewerPlugin(octoprint.plugin.SettingsPlugin,
                          octoprint.plugin.AssetPlugin,
						  octoprint.plugin.TemplatePlugin,
						  octoprint.plugin.BlueprintPlugin):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/KlipperViewer.js"],
			css=["css/KlipperViewer.css"],
			less=["less/KlipperViewer.less"]
		)

	##~~ BlueprintPlugin mixin
	@octoprint.plugin.BlueprintPlugin.route("/get_data", methods=["GET"])
	def get_data(self):
		parser = SerialParser(
			"/mnt/f/Geeetech/klipper/test.serial",
			"/mnt/f/Geeetech/klipper/out/klipper.dict",
			 self._logger
		)
		parser.parse()
		return flask.jsonify(parser.steps)
		#return flask.jsonify(parser.raw_messages)



	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			KlipperViewer=dict(
				displayName="Klipperviewer Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="fredizzimo",
				repo="KlipperViewer",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/fredizzimo/KlipperViewer/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Klipper Viewer"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = KlipperviewerPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

