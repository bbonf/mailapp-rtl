from distutils.core import setup
import py2app

plist = dict(NSPrincipalClass='MyPlugin',
	SupportedPluginCompatibilityUUIDs=['758F235A-2FD0-4660-9B52-102CD0EA897F','3335F782-01E2-4DF1-9E61-F81314124212',
	'608CE00F-4576-4CAD-B362-F3CCB7DE8D67','1146A009-E373-4DB6-AB4D-47E59A7E50FD'])

setup(
    plugin = ['plugin.py'],
    options=dict(py2app=dict(extension='.mailbundle', plist=plist))
 )