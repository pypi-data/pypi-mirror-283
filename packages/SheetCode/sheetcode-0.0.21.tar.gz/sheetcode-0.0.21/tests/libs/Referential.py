from enum import Enum

from lxml import etree as ET

referential = ET.parse("tests/referential/Routes.xml")

   
def Values(xpath):
    nodes = referential.xpath(xpath)
    return nodes

def Node(xpath):
    value = referential.xpath(xpath)[0]
    return True if value.lower() == "true" else False if value.lower() == "false" else value



    