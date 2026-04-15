import xml.etree.ElementTree as ET
import re
from xml.dom import minidom

ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
ET.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
# I HATE XML NAMESPACES I HATE XML NAMESPACES I HATE

def modify_svg(template_file, output_file, combination_number):
    tree = ET.parse(template_file)
    root = tree.getroot()
    
    # Determine the binary representation of the combination (reversed order)
    binary_string = f'{combination_number:09b}'[::-1]  # Reverse the string

    for i, state in enumerate(binary_string):
        dot_id = f'Dot{i + 1}'
        fill_color = '#000000' if state == '1' else '#FFFFFF'

        #find by id
        for element in root.findall(".//*[@id='{}']".format(dot_id)):
            if 'style' in element.attrib:
                style = element.attrib['style']
                style = re.sub(r'fill:[^;]*', f'fill:{fill_color}', style)
                element.set('style', style)
                # color gets changed here
            break 

    # Save the modified SVG to a new file without adding prefixes
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ET.tostring(root, encoding='utf-8').decode('utf-8'))

template_svg = 'template.svg'  
# Generate SVGs for all combinations from 1 to 512

for number in range(1, 513):
    output_svg = f'combination_{number}.svg'
    modify_svg(template_svg, output_svg, number)

print("SVG files generated for all combinations.")
