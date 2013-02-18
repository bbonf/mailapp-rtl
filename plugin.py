from AppKit import *
from Foundation import *
import objc
from ctypes import *
capi = pythonapi

main_menu = NSApplication.sharedApplication().mainMenu()
direction_menu = main_menu.itemAtIndex_(6).submenu().itemAtIndex_(5).submenu().itemAtIndex_(9).submenu()

class ButtonHandler(NSObject):
    def go_rtl(self):
        global direction_menu
        direction_menu.performActionForItemAtIndex_(3)

    def go_ltr(self):
        global direction_menu
        direction_menu.performActionForItemAtIndex_(2)

    def segment_action(self, sender):
        idx = sender.selectedSegment()
        if idx == 0:
            self.go_ltr()
        elif idx == 1:
            self.go_rtl()

        sender.setSelected_forSegment_(False,idx)

buttonHandler = ButtonHandler.alloc().init()

MailInspectorBarItemController = objc.lookUpClass('MailInspectorBarItemController')
class MailInspectorBarItemController(objc.Category(MailInspectorBarItemController)):
    @objc.signature(MailInspectorBarItemController.viewForInspectorBarItem_.signature)
    def myViewForInspectorBarItem_(self, arg):
        identifier = str(arg.identifier())
        
        if identifier == 'rtl_control':
            global buttonHandler
            
            btn = NSSegmentedControl.alloc().initWithFrame_(NSMakeRect(0.0,0.0,90.0,29.0))
            btn.cell().setControlSize_(1)
            btn.setSegmentCount_(2)
            btn.setSegmentStyle_(NSSegmentStyleTexturedRounded)
            btn.setFont_(NSFont.fontWithName_size_('LucidaGrande',9))
            btn.setLabel_forSegment_('LTR',0)
            btn.setWidth_forSegment_(28.0,0)
            btn.setLabel_forSegment_('RTL',1)
            btn.setWidth_forSegment_(28.0,1)

            btn.setTarget_(buttonHandler)
            btn.setAction_("segment_action")

            return btn

        return self.myViewForInspectorBarItem_(arg)
    	
    def supportedInspectorItemIdentifiers(self):
        return ['fontSizePopUp',  
                'textAlignment', 
                'list',
                'indentation',
                'rtl_control']

    supportedInspectorItemIdentifiers = classmethod(supportedInspectorItemIdentifiers)

EditingMessageWebView = objc.lookUpClass('EditingMessageWebView')
class EditingMessageWebView(objc.Category(EditingMessageWebView)):
    @objc.signature(EditingMessageWebView.inspectorBarItemIdentifiers.signature)
    def myInspectorBarItemIdentifiers(self):
        return ['NSInspectorBarFontFamilyItemIdentifier', 
                'NSInspectorBarSpaceItemIdentifier', 
                'fontSizePopUp', 'NSInspectorBarSpaceItemIdentifier', 
                'NSInspectorBarTextForegroundColorItemIdentifier', 
                'NSInspectorBarSpaceItemIdentifier', 
                'NSInspectorBarFontStyleItemIdentifier', 
                'NSInspectorBarSpaceItemIdentifier', 
                'textAlignment', 'NSInspectorBarSpaceItemIdentifier', 
                'list', 'NSInspectorBarSpaceItemIdentifier', 
                'indentation','NSInspectorBarSpaceItemIdentifier',
                'rtl_control']

capi.objc_getClass.restype = c_void_p
capi.objc_getClass.argtypes = [c_char_p]

capi.sel_registerName.restype = c_void_p
capi.sel_registerName.argtypes = [c_char_p]

def capi_get_selector(name):
    return c_void_p(capi.sel_registerName(name))

capi.class_getInstanceMethod.restype = c_void_p
capi.class_getInstanceMethod.argtypes = [c_void_p, c_void_p]

capi.method_exchangeImplementations.restype = None
capi.method_exchangeImplementations.argtypes = [c_void_p, c_void_p]

capi.class_getClassMethod.restype = c_void_p
capi.class_getClassMethod.argtypes = [c_void_p, c_void_p]

def hook(classname, orig, new):
    clazz = capi.objc_getClass(classname)
    
    origClose = capi.class_getInstanceMethod(clazz, capi_get_selector(orig))
    newClose = capi.class_getInstanceMethod(clazz, capi_get_selector(new))
    
    capi.method_exchangeImplementations(origClose, newClose)		

MVMailBundle = objc.lookUpClass('MVMailBundle')
class MyPlugin(MVMailBundle):
    def initialize (cls):
        MVMailBundle.registerBundle()
        NSLog("RTLButton registered with Mail")

        hook("MailInspectorBarItemController", "viewForInspectorBarItem:", "myViewForInspectorBarItem:")
        hook("EditingMessageWebView", "inspectorBarItemIdentifiers", "myInspectorBarItemIdentifiers")
        
    initialize = classmethod(initialize)