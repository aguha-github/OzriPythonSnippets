import xml.etree.cElementTree as ET
from error import Error

# represents an SDDraft file for altering settings
class SDDraft:

    def __init__(self, file_path):
        self.sddraft_file_path = file_path
        self.sddraft_tree = ET.parse(file_path)
        root = self.sddraft_tree.getroot()
        root.attrib["xmlns:typens"] = 'http://www.esri.com/schemas/ArcGIS/10.1'
        root.attrib["xmlns:xs"] = 'http://www.w3.org/2001/XMLSchema'

    # loads an sddraft file and returns the object
    @classmethod
    def load(sddraft, file_path):
        return sddraft(file_path)

    # saves the sddraft file
    def save(self):
        self.sddraft_tree.write(self.sddraft_file_path)

    # sets a property in the sddraft file
    def set_property(self, property_name, property_value):
        root = self.sddraft_tree.getroot()
        matched_properties = filter(lambda p: p.find('Key').text == property_name, root.findall('.//PropertySetProperty'))

        if len(matched_properties) == 0:
            raise PropertyNotFoundError(property_name)

        matched_properties[0].find('Value').text = property_value

    # sets the manifest type recorded in the sddraft file
    def set_manifest_type(self, type_value):
        root = self.sddraft_tree.getroot()
        elem = root.find('./Type')

        if elem is None:
            raise ElementNotFoundError('SVCManifest/Type')

        elem.text = type_value


class PropertyNotFoundError(Error):
    def __init__(self, property_name):
        self.property_name = property_name


class ElementNotFoundError(Error):
    def __init__(self, element_name):
        self.element_name = element_name