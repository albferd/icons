import xml.etree.ElementTree as ET
import re
from xml.dom import minidom
import sys
ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
ET.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
# I HATE XML NAMESPACES I HATE XML NAMESPACES I HATE

COLORS = ["#212121","#00b0ef","#ed008c", "#fef200"] # CMYK (black first)
# Add as many colors as you want here, and they'll be used as a base (the first will be used for missing digits)
N_DOTS = 9

def base_convert(i, b):
    result = []
    while i > 0:
            result.insert(0, i % b)
            i = i // b
    if result == []:
        return [0]
    return result
      
def modify_svg(template_file, output_file, combination_number):
    tree = ET.parse(template_file)
    root = tree.getroot()
    
    # Determine the base n representation of the combination (reversed order)
    numbers_array = base_convert(combination_number, len(COLORS))[::-1]  # Reverse the array
    if len(numbers_array) > N_DOTS:
        raise OverflowError(f"{combination_number} is too large to be represented with {N_DOTS} digits in base {len(COLORS)}")
    numbers_array = numbers_array + [0 for _ in range(N_DOTS-len(numbers_array))] # Fill with 0s until there are 9 digits
    
    for i, state in enumerate(numbers_array):
        dot_id = f'Dot{i + 1}'
        fill_color = COLORS[numbers_array[i]]

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

if len(sys.argv) not in (3,4):
    print(f'''Usage:
    {sys.argv[0]} <template_file> <number>
    or
    {sys.argv[0]} <template_file> <range_start> <range_end>
    ''')
    exit(1)
if len(sys.argv) == 3:
    output_svg = f'{sys.argv[2]}.svg'
    
    modify_svg(sys.argv[1], output_svg, int(sys.argv[2]))
    print(f"Done :) generated svg no.{sys.argv[2]}")
    exit(0)
if len(sys.argv) == 4:
    for number in range(int(sys.argv[2]), int(sys.argv[3])):
        output_svg = f'{number}.svg'
        modify_svg(sys.argv[1], output_svg, number)
    print("SVG files generated for all combinations.")

    
