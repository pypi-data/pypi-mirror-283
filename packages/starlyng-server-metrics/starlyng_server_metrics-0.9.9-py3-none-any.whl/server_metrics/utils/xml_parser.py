"""
xml_parser.py
"""
import logging
import xml.etree.ElementTree as ET
from typing import Dict, List

class XMLProcessingError(Exception):
    """Custom exception for errors during XML processing"""

def xml_to_json(xml_data: str) -> Dict[str, any]:
    """
    Converts xml to json

    Args:
        xml_data (str):

    Returns:
        Dict[str, any]:
    """
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        logging.error("Error parsing XML: %s\n%s", e, xml_data)
        return {}

    def recurse_node(node):
        result = {}
        if node.text and node.text.strip():
            result['text'] = node.text.strip()
        for child in node:
            child_result = recurse_node(child)
            if child.tag in result:
                if isinstance(result[child.tag], List):
                    result[child.tag].append(child_result)
                else:
                    result[child.tag] = [result[child.tag], child_result]
            else:
                result[child.tag] = child_result
        return result

    try:
        return recurse_node(root)
    except XMLProcessingError as e:
        logging.error("Error processing XML: %s", e)
        return {}
